#!/usr/bin/env python3
"""MCP client + CLI for the Minefort Citadel MCP server.

Speaks the Model Context Protocol (2025-06-18) over Streamable HTTP
against https://minefort.com/mcp, with OAuth 2.1 PKCE bootstrap, dynamic
client registration (RFC 7591), and a refresh-token-aware credential
cache at .secrets/minefort_mcp_token.json.

The Minefort MCP server (https://minefort.com/docs/mcp) exposes ~30 tools
spanning server management, file/console ops, build inspection, publishing,
backups, and in-game sales. Every tool is reachable two ways:

    # generic form — works for any tool the server exposes
    python3 scripts/minefort_mcp.py call list_workloads
    python3 scripts/minefort_mcp.py call power \
        --arg workload=<id> --arg action=restart

    # convenience alias — same call, friendlier CLI
    python3 scripts/minefort_mcp.py list-workloads
    python3 scripts/minefort_mcp.py power <id> restart

Token cache layout (.secrets/minefort_mcp_token.json, mode 600):
    {
      "client_id": "...",         # from DCR, one-time
      "access_token": "...",
      "refresh_token": "...",     # if offline_access was granted
      "token_type": "Bearer",
      "expires_at": 1735689600,   # unix epoch seconds
      "scope": "workloads offline_access",
      "obtained_at": 1735686000
    }

The cache is ALSO mirrored into .git/config (key sync.minefortmcptoken)
because .secrets/ can be wiped by container recycles while .git/
demonstrably survives (same trick git_sync.py uses for the GitHub
token). _load_token_cache() restores from the mirror automatically.

HEADLESS / REMOTE-BROWSER AUTH (manual relay):
The default `auth` flow needs a browser AND a localhost listener on the
same machine — impossible when this script runs in a container but the
operator's browser is elsewhere. The relay flow splits it in two:

    # step 1 (container): prints the sign-in URL, stashes PKCE verifier
    python3 scripts/minefort_mcp.py auth --manual

    # step 2 (operator): open the URL, sign in; the browser lands on a
    # dead http://127.0.0.1:<port>/callback?code=...&state=... page —
    # copy that WHOLE address-bar URL

    # step 3 (container): finish the exchange with the pasted URL
    python3 scripts/minefort_mcp.py auth --complete '<pasted URL>'

PKCE (S256) still protects the exchange; state is validated against the
stashed value, so a stale pasted URL from an older --manual run is
rejected.

Exit codes:
    0  success
    1  usage error
    2  OAuth required (no cached token, or refresh failed)
    3  MCP call returned an error response
    4  network/transport error
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import http.server
import json
import os
import secrets as pysecrets
import subprocess
import sys
import threading
import time
import urllib.parse
import webbrowser
from typing import Any

try:
    import requests
except ModuleNotFoundError:  # pragma: no cover - bootstrap, like git_ssh.py
    sys.stderr.write("minefort_mcp.py: requests missing — auto-installing...\n")
    import subprocess
    _r = subprocess.run(
        [sys.executable, "-m", "pip", "install", "--quiet",
         "--disable-pip-version-check", "--no-input", "requests"],
        capture_output=True, text=True,
    )
    if _r.returncode != 0:
        sys.stderr.write(
            f"minefort_mcp.py: auto-install failed: "
            f"{(_r.stderr or _r.stdout).strip()}\n"
        )
        sys.exit(4)
    import requests  # type: ignore

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRETS_DIR = os.path.join(PROJECT_ROOT, ".secrets")
TOKEN_PATH = os.path.join(SECRETS_DIR, "minefort_mcp_token.json")
# Out-of-band relay state (verifier + state + client_id) between
# `auth --manual` and `auth --complete`.
PENDING_PATH = os.path.join(SECRETS_DIR, "minefort_mcp_pending.json")
# Durable mirror of the token cache. .git/config is never committed to
# the remote (it is repo-local), and it survives container recycles that
# have wiped .secrets/ in the past (see git_sync.py's docstring).
GIT_CONFIG_KEY = "sync.minefortmcptoken"

MCP_ENDPOINT = "https://minefort.com/mcp"
PROTECTED_RESOURCE = "https://minefort.com/.well-known/oauth-protected-resource/mcp"
AS_METADATA_URL = "https://minefort.com/.well-known/oauth-authorization-server"

PROTOCOL_VERSION = "2025-06-18"
CLIENT_INFO = {"name": "citadel-docs-mcp-cli", "version": "0.1.0"}
DEFAULT_SCOPE = "workloads offline_access"
# RFC 8707 resource indicator — Minefort's DCR response includes
# "resources": ["https://minefort.com/mcp"], and the AS may reject
# token exchange without this parameter (invalid_target). Bind every
# authorize + token request to the MCP resource explicitly.
RESOURCE_INDICATOR = MCP_ENDPOINT
CALLBACK_PORT = 0  # 0 = pick any free port
CALLBACK_TIMEOUT = 300  # 5 min to complete browser sign-in

# Exit codes (mirrored from module docstring).
EXIT_OK = 0
EXIT_USAGE = 1
EXIT_OAUTH_REQUIRED = 2
EXIT_MCP_ERROR = 3
EXIT_NETWORK = 4

# ---------------------------------------------------------------------------
# Logging helpers
# ---------------------------------------------------------------------------

def _warn(msg: str) -> None:
    sys.stderr.write(f"minefort_mcp.py: {msg}\n")
    sys.stderr.flush()


def _die(msg: str, code: int = EXIT_USAGE) -> None:
    _warn(msg)
    sys.exit(code)


# ---------------------------------------------------------------------------
# OAuth 2.1 PKCE + Dynamic Client Registration
# ---------------------------------------------------------------------------

def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _make_pkce() -> tuple[str, str]:
    """Return (code_verifier, code_challenge) per RFC 7636 S256."""
    verifier = _b64url(pysecrets.token_bytes(64))
    # verifier charset must be [A-Z / a-z / 0-9 - . _ ~], length 43-128.
    # 64 raw bytes -> 86 b64url chars: in range.
    challenge = _b64url(
        hashlib.sha256(verifier.encode("ascii")).digest()
    )
    return verifier, challenge


def _atomic_write_json(path: str, obj: Any, mode: int = 0o600) -> None:
    """Write JSON to path atomically (tmp + rename) and chmod it."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    os.chmod(os.path.dirname(path), 0o700)
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=2, sort_keys=True)
        f.write("\n")
    os.chmod(tmp, mode)
    os.replace(tmp, path)


def _git_config_get_token() -> dict | None:
    """Read the durable token mirror from .git/config, if present."""
    try:
        r = subprocess.run(
            ["git", "-C", PROJECT_ROOT, "config", "--get", GIT_CONFIG_KEY],
            capture_output=True, text=True, timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if r.returncode != 0 or not r.stdout.strip():
        return None
    try:
        return json.loads(r.stdout.strip())
    except json.JSONDecodeError:
        _warn("git-config token mirror is corrupt; ignoring it")
        return None


def _git_config_set_token(tok: dict) -> None:
    """Mirror the token cache into .git/config (survives .secrets/ wipes)."""
    compact = json.dumps(tok, sort_keys=True, separators=(",", ":"))
    try:
        subprocess.run(
            ["git", "-C", PROJECT_ROOT, "config", GIT_CONFIG_KEY, compact],
            capture_output=True, timeout=10, check=True,
        )
    except (OSError, subprocess.SubprocessError) as e:
        _warn(f"could not mirror token into .git/config ({e}) — "
              f"only {TOKEN_PATH} holds it")


def _load_token_cache() -> dict | None:
    if os.path.exists(TOKEN_PATH):
        try:
            with open(TOKEN_PATH) as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            _warn(f"token cache unreadable ({e}); trying git-config mirror")
    # .secrets/ was wiped (container recycle) or file is corrupt — the
    # .git/config mirror keeps the refresh_token alive across recycles.
    return _git_config_get_token()


def _save_token_cache(tok: dict) -> None:
    tok["obtained_at"] = int(time.time())
    _atomic_write_json(TOKEN_PATH, tok, mode=0o600)
    _git_config_set_token(tok)


def _register_client(as_meta: dict) -> str:
    """RFC 7591 dynamic client registration; returns client_id.

    Minefort's AS advertises `registration_endpoint` and supports
    `token_endpoint_auth_methods_supported: ["none", ...]`, so we register
    as a public client (no secret). The registration is persisted in the
    token cache so it only happens once.
    """
    url = as_meta["registration_endpoint"]
    body = {
        "client_name": "citadel-docs-mcp-cli",
        "redirect_uris": [_local_callback_url_hint()],
        "grant_types": ["authorization_code", "refresh_token"],
        "token_endpoint_auth_method": "none",
        "scope": DEFAULT_SCOPE,
        "response_types": ["code"],
    }
    resp = requests.post(url, json=body, timeout=30)
    if resp.status_code >= 400:
        raise RuntimeError(
            f"DCR failed ({resp.status_code} {resp.reason}): {resp.text[:400]}"
        )
    data = resp.json()
    cid = data.get("client_id")
    if not cid:
        raise RuntimeError(f"DCR response missing client_id: {data}")
    return cid


def _local_callback_url_hint() -> str:
    """The literal redirect_uri we'll register and use. We bind to
    127.0.0.1 with a fixed port derived from a project-specific hash so
    the same port is reused across runs (otherwise DCR would need a new
    client_id every time). Falls back to 8374 if anything weird happens."""
    # Stable port in the dynamic/ephemeral range (49152-65535).
    h = hashlib.sha1(PROJECT_ROOT.encode()).digest()
    port = 49152 + (int.from_bytes(h[:2], "big") % 16384)
    return f"http://127.0.0.1:{port}/callback"


class _CallbackHandler(http.server.BaseHTTPRequestHandler):
    """Capture ?code=...&state=... from the OAuth redirect."""

    def log_message(self, *args):  # silence default stderr spam
        pass

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        code = params.get("code", [None])[0]
        state = params.get("state", [None])[0]
        err = params.get("error", [None])[0]
        # Stash on the server instance so the main thread can read it.
        self.server.received = {"code": code, "state": state, "error": err}  # type: ignore
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        if err:
            body = (
                f"<h2>Authorization failed</h2><p>Error: {err}</p>"
                f"<p>You can close this tab.</p>"
            )
        elif code:
            body = (
                "<h2>Authorized</h2>"
                "<p>You can close this tab and return to the terminal.</p>"
            )
        else:
            body = "<h2>Waiting...</h2>"
        self.wfile.write(body.encode("utf-8"))


def _wait_for_callback(
    port: int, expected_state: str, timeout: int = CALLBACK_TIMEOUT
) -> str:
    """Block until the OAuth redirect lands; return the authorization code."""
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", port), _CallbackHandler)
    srv.received = {}  # type: ignore
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    deadline = time.time() + timeout
    try:
        while time.time() < deadline:
            rcv = getattr(srv, "received", {}) or {}
            if rcv.get("code") or rcv.get("error"):
                break
            time.sleep(0.25)
        rcv = getattr(srv, "received", {}) or {}
    finally:
        srv.shutdown()
        srv.server_close()
    if rcv.get("error"):
        raise RuntimeError(
            f"OAuth provider returned error: {rcv['error']} "
            f"({rcv.get('error_description', '')})"
        )
    code = rcv.get("code")
    if not code:
        raise RuntimeError(
            f"OAuth callback timed out after {timeout}s — "
            f"did you complete the sign-in in the browser?"
        )
    if rcv.get("state") != expected_state:
        raise RuntimeError("OAuth state mismatch — possible CSRF, aborting")
    return code


def _exchange_code(
    as_meta: dict, client_id: str, code: str,
    redirect_uri: str, verifier: str,
) -> dict:
    """Exchange the authorization code for tokens; returns the raw token JSON."""
    resp = requests.post(
        as_meta["token_endpoint"],
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "code_verifier": verifier,
            # RFC 8707 resource indicator — binds the access token to the
            # MCP endpoint. The AS advertised this resource via DCR.
            "resource": RESOURCE_INDICATOR,
        },
        headers={"Accept": "application/json"},
        timeout=30,
    )
    if resp.status_code >= 400:
        raise RuntimeError(
            f"token exchange failed ({resp.status_code} {resp.reason}): "
            f"{resp.text[:400]}"
        )
    data = resp.json()
    if "access_token" not in data:
        raise RuntimeError(f"token response missing access_token: {data}")
    # Absolute expiry so refresh logic is unambiguous.
    if "expires_in" in data and "expires_at" not in data:
        data["expires_at"] = int(time.time()) + int(data["expires_in"])
    return data


def _refresh_token(as_meta: dict, client_id: str, refresh_tok: str) -> dict:
    resp = requests.post(
        as_meta["token_endpoint"],
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_tok,
            "client_id": client_id,
            "scope": DEFAULT_SCOPE,
            "resource": RESOURCE_INDICATOR,
        },
        headers={"Accept": "application/json"},
        timeout=30,
    )
    if resp.status_code >= 400:
        raise RuntimeError(
            f"token refresh failed ({resp.status_code} {resp.reason}): "
            f"{resp.text[:400]}"
        )
    data = resp.json()
    if "expires_in" in data and "expires_at" not in data:
        data["expires_at"] = int(time.time()) + int(data["expires_in"])
    # Some ASes don't return a new refresh_token; preserve the old one.
    if "refresh_token" not in data:
        data["refresh_token"] = refresh_tok
    return data


def _parse_callback_port(redirect_uri: str) -> int:
    parsed = urllib.parse.urlparse(redirect_uri)
    return int(parsed.port) if parsed.port else 80


def do_oauth_flow(force: bool = False) -> dict:
    """Run the full OAuth flow if needed, or refresh on a cache hit.

    Returns the live token dict (always contains a usable access_token).
    Raises RuntimeError on any unrecoverable failure.
    """
    as_meta = requests.get(AS_METADATA_URL, timeout=15).json()
    cache = _load_token_cache()

    # Fast path: cached token still valid (with 60s safety margin).
    if cache and not force:
        exp = cache.get("expires_at", 0)
        if exp > time.time() + 60:
            return cache
        # Try refresh.
        if cache.get("refresh_token"):
            try:
                tok = _refresh_token(
                    as_meta, cache["client_id"], cache["refresh_token"]
                )
                tok["client_id"] = cache["client_id"]
                _save_token_cache(tok)
                return tok
            except RuntimeError as e:
                _warn(f"token refresh failed ({e}); forcing full re-auth")

    # Full flow: DCR (if no cached client_id) -> authorize -> exchange.
    # In headless / cron contexts this must not block on a browser we
    # cannot open. MINEFORT_MCP_NONINTERACTIVE=1 forces a clean exit
    # instead, so the operator can `auth` interactively first.
    non_interactive = os.environ.get("MINEFORT_MCP_NONINTERACTIVE") == "1"
    if non_interactive:
        raise RuntimeError(
            "no usable cached token and MINEFORT_MCP_NONINTERACTIVE=1 is set; "
            "bootstrap with `python3 scripts/minefort_mcp.py auth --manual` "
            "(relay flow for headless hosts) or plain `auth` on a machine "
            "with a browser"
        )

    client_id = (cache or {}).get("client_id")
    if not client_id:
        client_id = _register_client(as_meta)

    verifier, challenge = _make_pkce()
    state = pysecrets.token_urlsafe(24)
    redirect_uri = _local_callback_url_hint()
    port = _parse_callback_port(redirect_uri)

    auth_url = as_meta["authorization_endpoint"]
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": DEFAULT_SCOPE,
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        # RFC 8707 resource indicator — bound to the MCP endpoint so the
        # AS issues a token that's only valid against https://minefort.com/mcp.
        "resource": RESOURCE_INDICATOR,
    }
    full = f"{auth_url}?{urllib.parse.urlencode(params)}"

    print(f"\n[oauth] opening browser to sign in to Minefort...")
    print(f"[oauth] if the browser doesn't open, visit this URL manually:")
    print(f"[oauth]   {full}\n")
    opened = False
    try:
        opened = bool(webbrowser.open(full))
    except Exception:
        opened = False
    if not opened:
        # Headless host: the redirect will land on the OPERATOR's
        # localhost, never on ours — the listener below can only fire if
        # this script and the browser share a machine. Don't make the
        # operator wait the full CALLBACK_TIMEOUT for nothing; point at
        # the relay flow, which needs no listener at all.
        print(
            "[oauth] no browser on this host — the localhost callback "
            "will NOT reach us. Waiting only 90s in case a browser is "
            "shared; if that fails use the relay flow:\n"
            "[oauth]   python3 scripts/minefort_mcp.py auth --manual\n"
        )
    code = _wait_for_callback(
        port, state,
        timeout=CALLBACK_TIMEOUT if opened else 90,
    )
    tok = _exchange_code(as_meta, client_id, code, redirect_uri, verifier)
    tok["client_id"] = client_id
    _save_token_cache(tok)
    return tok


def require_token(force: bool = False) -> dict:
    """Like do_oauth_flow but exits with EXIT_OAUTH_REQUIRED on failure so
    the CLI can distinguish auth problems from real errors."""
    try:
        return do_oauth_flow(force=force)
    except RuntimeError as e:
        _die(f"OAuth failed: {e}", code=EXIT_OAUTH_REQUIRED)


# ---------------------------------------------------------------------------
# Out-of-band manual relay (headless hosts, remote browser)
# ---------------------------------------------------------------------------

def start_manual_auth(as_meta: dict, cache: dict | None) -> None:
    """Begin the relay flow: print the sign-in URL, stash verifier+state.

    Same DCR + PKCE machinery as the browser flow, but no localhost
    listener — impossible to reach when the operator's browser runs on a
    different machine than this script (the container case). The operator
    completes sign-in, their browser lands on a dead 127.0.0.1 callback
    page whose address bar contains ?code=...&state=..., and they paste
    that URL back for `auth --complete` to finish the exchange.
    """
    client_id = (cache or {}).get("client_id")
    if not client_id:
        client_id = _register_client(as_meta)

    verifier, challenge = _make_pkce()
    state = pysecrets.token_urlsafe(24)
    redirect_uri = _local_callback_url_hint()

    _atomic_write_json(PENDING_PATH, {
        "client_id": client_id,
        "verifier": verifier,
        "state": state,
        "redirect_uri": redirect_uri,
        "created_at": int(time.time()),
    }, mode=0o600)

    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": DEFAULT_SCOPE,
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "resource": RESOURCE_INDICATOR,
    }
    full = f"{as_meta['authorization_endpoint']}?{urllib.parse.urlencode(params)}"

    print("[manual] relay flow started — pending state stashed at:")
    print(f"[manual]   {PENDING_PATH}")
    print()
    print("[manual] STEP 1 — open this URL in ANY browser and sign in:")
    print(f"[manual]   {full}")
    print()
    print("[manual] STEP 2 — after sign-in the browser redirects to")
    print("[manual]   http://127.0.0.1:<port>/callback?code=...&state=...")
    print("[manual] which will show a connection-refused / dead page. That's")
    print("[manual] EXPECTED — the auth code is in the address bar. Copy the")
    print("[manual] ENTIRE URL from the address bar.")
    print()
    print("[manual] STEP 3 — finish with the pasted URL:")
    print("[manual]   python3 scripts/minefort_mcp.py auth --complete '<pasted URL>'")
    print()
    print("[manual] codes expire fast (minutes). If the exchange fails, just")
    print("[manual] re-run auth --manual for a fresh URL.")


def complete_manual_auth(pasted: str) -> int:
    """Finish the relay flow with the pasted callback URL (or bare code)."""
    pasted = pasted.strip().strip('"').strip("'").strip()
    code: str | None = None
    state: str | None = None
    if pasted.startswith("http"):
        parsed = urllib.parse.urlparse(pasted)
        q = urllib.parse.parse_qs(parsed.query)
        err = (q.get("error") or [None])[0]
        if err:
            _die(
                f"provider returned error in callback: {err} "
                f"({(q.get('error_description') or [''])[0]})",
                code=EXIT_OAUTH_REQUIRED,
            )
        code = (q.get("code") or [None])[0]
        state = (q.get("state") or [None])[0]
    else:
        code = pasted  # bare code pasted without the wrapper URL
    if not code:
        _die("could not find ?code= in the pasted URL", code=EXIT_OAUTH_REQUIRED)

    if not os.path.exists(PENDING_PATH):
        _die(
            "no pending relay auth found — the container may have recycled "
            "between --manual and --complete. Start over with: "
            "auth --manual",
            code=EXIT_OAUTH_REQUIRED,
        )
    with open(PENDING_PATH) as f:
        pending = json.load(f)
    if state is not None and state != pending.get("state"):
        _die(
            "state mismatch — this URL belongs to an older auth --manual "
            "run. Re-run auth --manual and use the newest URL",
            code=EXIT_OAUTH_REQUIRED,
        )

    as_meta = requests.get(AS_METADATA_URL, timeout=15).json()
    try:
        tok = _exchange_code(
            as_meta, pending["client_id"], code,
            pending["redirect_uri"], pending["verifier"],
        )
    except RuntimeError as e:
        _die(
            f"code exchange failed: {e}\n"
            f"authorization codes are short-lived and single-use — re-run "
            f"auth --manual and paste promptly",
            code=EXIT_OAUTH_REQUIRED,
        )
    tok["client_id"] = pending["client_id"]
    _save_token_cache(tok)
    try:
        os.unlink(PENDING_PATH)
    except OSError:
        pass

    exp = tok.get("expires_at", 0)
    when = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(exp)) if exp else "?"
    print("[manual] exchange OK — token cached:")
    print(f"[manual]   {TOKEN_PATH}")
    print(f"[manual]   (.git/config mirror under {GIT_CONFIG_KEY})")
    print(f"[manual] scope: {tok.get('scope', DEFAULT_SCOPE)}")
    print(f"[manual] expires_at: {when}")
    print(f"[manual] refresh_token present: {bool(tok.get('refresh_token'))}")
    print("[manual] try: python3 scripts/minefort_mcp.py list-tools")
    return EXIT_OK


# ---------------------------------------------------------------------------
# MCP JSON-RPC client (Streamable HTTP)
# ---------------------------------------------------------------------------

class MCPSession:
    """A minimal MCP Streamable-HTTP client.

    Handles initialize / notifications/initialized / tools/list / tools/call.
    Captures Mcp-Session-Id when the server returns one and resends it on
    every subsequent request, per the spec.
    """

    def __init__(self, token: str, endpoint: str = MCP_ENDPOINT):
        self.endpoint = endpoint
        self.token = token
        self.session_id: str | None = None
        self.protocol_version: str = PROTOCOL_VERSION
        self._next_id = 1
        self._init_ok = False

    def _headers(self, extra: dict | None = None) -> dict:
        h = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "MCP-Protocol-Version": self.protocol_version,
        }
        if self.session_id:
            h["Mcp-Session-Id"] = self.session_id
        if extra:
            h.update(extra)
        return h

    def _next_request_id(self) -> int:
        rid = self._next_id
        self._next_id += 1
        return rid

    @staticmethod
    def _parse_response(resp: requests.Response) -> dict:
        """Extract the JSON-RPC payload from either a single JSON response
        or a text/event-stream with `data:` frames."""
        ctype = (resp.headers.get("content-type") or "").lower()
        if "application/json" in ctype:
            return resp.json()
        if "text/event-stream" in ctype:
            buf = []
            for line in resp.iter_lines(decode_unicode=True):
                if not line:
                    continue
                if line.startswith("data:"):
                    payload = line[5:].lstrip()
                    try:
                        ev = json.loads(payload)
                    except json.JSONDecodeError:
                        continue
                    # An event that carries a JSON-RPC response has an id
                    # (response) or an `error` (notification). Skip
                    # notifications and progress events; return the first
                    # real response.
                    if isinstance(ev, dict) and ("id" in ev or "result" in ev or "error" in ev):
                        buf.append(ev)
            if len(buf) == 1:
                return buf[0]
            if not buf:
                raise RuntimeError(
                    f"SSE stream carried no JSON-RPC response "
                    f"(status {resp.status_code})"
                )
            # Multiple — return the last (server-sent `result` overwrites
            # interim progress notifications, which we filtered out above
            # anyway).
            return buf[-1]
        # Fallback: best-effort JSON parse
        try:
            return resp.json()
        except ValueError:
            raise RuntimeError(
                f"unexpected content-type {ctype!r}; body: {resp.text[:400]}"
            )

    def _post(self, payload: dict) -> dict:
        try:
            resp = requests.post(
                self.endpoint, headers=self._headers(),
                json=payload, timeout=120,
            )
        except requests.RequestException as e:
            _die(f"network error: {e}", code=EXIT_NETWORK)
        # Capture session id once, on the initialize response.
        sid = resp.headers.get("Mcp-Session-Id")
        if sid and not self.session_id:
            self.session_id = sid
        pv = resp.headers.get("MCP-Protocol-Version")
        if pv:
            self.protocol_version = pv
        if resp.status_code == 401:
            _die(
                "server returned 401 — token rejected or expired. "
                "Re-run: python3 scripts/minefort_mcp.py auth --force",
                code=EXIT_OAUTH_REQUIRED,
            )
        if resp.status_code >= 400:
            _die(
                f"HTTP {resp.status_code} {resp.reason}: {resp.text[:400]}",
                code=EXIT_NETWORK,
            )
        return self._parse_response(resp)

    def initialize(self) -> dict:
        rid = self._next_request_id()
        resp = self._post({
            "jsonrpc": "2.0", "id": rid, "method": "initialize",
            "params": {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"roots": {"listChanged": True}},
                "clientInfo": CLIENT_INFO,
            },
        })
        if "error" in resp:
            _die(
                f"initialize error: {resp['error']}",
                code=EXIT_MCP_ERROR,
            )
        result = resp.get("result", {})
        # Send the initialized notification (no response expected).
        try:
            requests.post(
                self.endpoint, headers=self._headers(),
                json={
                    "jsonrpc": "2.0",
                    "method": "notifications/initialized",
                },
                timeout=30,
            )
        except requests.RequestException:
            pass  # non-fatal
        self._init_ok = True
        return result

    def list_tools(self) -> list[dict]:
        if not self._init_ok:
            self.initialize()
        rid = self._next_request_id()
        resp = self._post({
            "jsonrpc": "2.0", "id": rid, "method": "tools/list",
            "params": {},
        })
        if "error" in resp:
            _die(f"tools/list error: {resp['error']}", code=EXIT_MCP_ERROR)
        return resp.get("result", {}).get("tools", [])

    def call_tool(self, name: str, arguments: dict | None = None) -> dict:
        if not self._init_ok:
            self.initialize()
        rid = self._next_request_id()
        resp = self._post({
            "jsonrpc": "2.0", "id": rid, "method": "tools/call",
            "params": {"name": name, "arguments": arguments or {}},
        })
        if "error" in resp:
            err = resp["error"]
            _die(
                f"tools/call '{name}' error: "
                f"{err.get('message') or err} (code {err.get('code')})",
                code=EXIT_MCP_ERROR,
            )
        return resp.get("result", {})


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_kv_arg(s: str) -> tuple[str, str]:
    """Parse `--arg key=value`. Empty value is allowed."""
    if "=" not in s:
        raise argparse.ArgumentTypeError(
            f"--arg expects key=value, got {s!r}"
        )
    k, v = s.split("=", 1)
    if not k:
        raise argparse.ArgumentTypeError(
            f"--arg key must be non-empty, got {s!r}"
        )
    return k, v


def _coerce_value(v: str) -> Any:
    """Best-effort: 'true'/'false' -> bool, digits -> int, valid JSON -> parsed."""
    if v.lower() == "true":
        return True
    if v.lower() == "false":
        return False
    if v == "null":
        return None
    # Integer
    try:
        return int(v, 10)
    except ValueError:
        pass
    # JSON object / array / number / quoted string
    if v and v[0] in "{[\"":
        try:
            return json.loads(v)
        except json.JSONDecodeError:
            pass
    return v


def _format_result(result: dict) -> str:
    """Render an MCP tool-call result for terminal display.

    MCP `tools/call` returns:
        {
          "content": [{"type": "text", "text": "..."}, ...],
          "isError": false
        }
    We pretty-print text content and fall back to JSON for anything else.
    """
    if not isinstance(result, dict):
        return json.dumps(result, indent=2)
    content = result.get("content")
    if isinstance(content, list) and content:
        parts = []
        for blk in content:
            if isinstance(blk, dict) and blk.get("type") == "text":
                parts.append(blk.get("text", ""))
            else:
                parts.append(json.dumps(blk, indent=2))
        joined = "\n".join(parts)
        if result.get("isError"):
            return f"[MCP error response]\n{joined}"
        return joined
    # Some servers return the result inline (non-spec but tolerate it).
    return json.dumps(result, indent=2, sort_keys=True)


# ----- subcommands ---------------------------------------------------------

def cmd_auth(args) -> int:
    """Perform (or refresh) the OAuth flow and cache the token."""
    if getattr(args, "complete", None):
        return complete_manual_auth(args.complete)
    if getattr(args, "manual", False):
        as_meta = requests.get(AS_METADATA_URL, timeout=15).json()
        start_manual_auth(as_meta, _load_token_cache())
        return EXIT_OK
    tok = require_token(force=args.force)
    exp = tok.get("expires_at", 0)
    when = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(exp)) if exp else "?"
    print(f"[auth] token cached at {TOKEN_PATH}")
    print(f"[auth] scope: {tok.get('scope', DEFAULT_SCOPE)}")
    print(f"[auth] expires_at: {when}")
    print(f"[auth] refresh_token present: {bool(tok.get('refresh_token'))}")
    return EXIT_OK


def cmd_whoami(args) -> int:
    tok = require_token()
    as_meta = requests.get(AS_METADATA_URL, timeout=15).json()
    ui = as_meta.get("userinfo_endpoint")
    if not ui:
        _die("AS metadata has no userinfo_endpoint", code=EXIT_USAGE)
    resp = requests.get(
        ui, headers={"Authorization": f"Bearer {tok['access_token']}"},
        timeout=30,
    )
    if resp.status_code >= 400:
        _die(f"userinfo failed ({resp.status_code}): {resp.text[:300]}",
             code=EXIT_NETWORK)
    print(json.dumps(resp.json(), indent=2, sort_keys=True))
    return EXIT_OK


def cmd_list_tools(args) -> int:
    tok = require_token()
    sess = MCPSession(tok["access_token"])
    tools = sess.list_tools()
    if args.json:
        print(json.dumps(tools, indent=2, sort_keys=True))
        return EXIT_OK
    if not tools:
        print("(server returned no tools)")
        return EXIT_OK
    print(f"{len(tools)} tools available from {MCP_ENDPOINT}:\n")
    width = max(len(t["name"]) for t in tools)
    for t in sorted(tools, key=lambda x: x["name"]):
        desc = (t.get("description") or "").strip().splitlines()
        summary = desc[0] if desc else ""
        print(f"  {t['name'].ljust(width)}  {summary}")
    return EXIT_OK


def cmd_call(args) -> int:
    tok = require_token()
    sess = MCPSession(tok["access_token"])
    arguments: dict[str, Any] = {}
    for k, v in args.args:
        arguments[k] = _coerce_value(v)
    if args.json_input:
        # Merge JSON blob from stdin under `arguments` (overrides --arg).
        try:
            blob = json.load(sys.stdin)
        except json.JSONDecodeError as e:
            _die(f"--json-input: stdin is not valid JSON ({e})",
                 code=EXIT_USAGE)
        if not isinstance(blob, dict):
            _die("--json-input: stdin must be a JSON object",
                 code=EXIT_USAGE)
        arguments.update(blob)
    result = sess.call_tool(args.tool, arguments)
    if args.raw:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(_format_result(result))
    return EXIT_OK


def _make_convenience_runner(tool_name: str, arg_order: list[str]):
    """Build a subcommand handler that maps positional CLI args to
    MCP tool arguments in the given order, with optional --flag extras."""

    def handler(args) -> int:
        tok = require_token()
        sess = MCPSession(tok["access_token"])
        arguments: dict[str, Any] = {}
        positional = [a for a in vars(args).get("_positional", [])]
        for i, name in enumerate(arg_order):
            if i < len(positional):
                arguments[name] = _coerce_value(positional[i])
        # Merged extras from --arg
        for k, v in getattr(args, "args", []) or []:
            arguments[k] = _coerce_value(v)
        result = sess.call_tool(tool_name, arguments)
        if getattr(args, "raw", False):
            print(json.dumps(result, indent=2, sort_keys=True))
        else:
            print(_format_result(result))
        return EXIT_OK

    return handler


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="minefort_mcp.py",
        description=(
            "MCP client + CLI for the Minefort Citadel MCP server "
            "(https://minefort.com/mcp). Run `auth` first to bootstrap "
            "OAuth, then `list-tools` or any convenience subcommand."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = p.add_subparsers(dest="command", metavar="<command>")

    # auth
    pa = sub.add_parser("auth", help="perform or refresh the OAuth flow")
    pa.add_argument("--force", action="store_true",
                    help="discard cached token and re-authenticate")
    pa.add_argument("--manual", action="store_true",
                    help="headless relay: print a sign-in URL and stash "
                         "PKCE state; complete later with --complete")
    pa.add_argument("--complete", metavar="CALLBACK_URL",
                    help="finish the --manual relay flow using the pasted "
                         "callback URL (or a bare authorization code)")
    pa.set_defaults(func=cmd_auth)

    # whoami
    pw = sub.add_parser("whoami", help="print the OAuth userinfo endpoint output")
    pw.set_defaults(func=cmd_whoami)

    # list-tools
    pt = sub.add_parser("list-tools", help="list tools exposed by the MCP server")
    pt.add_argument("--json", action="store_true", help="raw JSON output")
    pt.set_defaults(func=cmd_list_tools)

    # call (generic)
    pc = sub.add_parser(
        "call", help="call any MCP tool by name",
        description=(
            "Call any tool the server exposes. Arguments are passed as "
            "key=value strings (with light type coercion: true/false/null, "
            "integers, and JSON-prefixed objects/arrays decode; everything "
            "else stays a string). For complex arguments, pipe a JSON "
            "object on stdin with --json-input."
        ),
    )
    pc.add_argument("tool", help="MCP tool name (e.g. list_workloads)")
    pc.add_argument("--arg", "-a", action="append", default=[],
                    type=_parse_kv_arg, metavar="KEY=VALUE",
                    help="tool argument (repeatable)")
    pc.add_argument("--json-input", action="store_true",
                    help="merge a JSON object from stdin into the arguments")
    pc.add_argument("--raw", action="store_true",
                    help="print the raw MCP result envelope as JSON")
    pc.set_defaults(func=cmd_call)

    # ----- Convenience aliases for the documented Minefort tools -----
    # Each entry: (subcommand_name, MCP tool name, positional arg names,
    #              help, extras_help).
    convenience = [
        # Server management
        ("list-workloads", "list_workloads", [],
         "list all Citadel workloads you can manage", None),
        ("get-workload", "get_workload", ["workload"],
         "show details for one workload", None),
        ("list-software", "list_software", [],
         "list Citadel software versions available for provisioning", None),
        ("create-workload", "create_workload", [],
         "create a workload (use --arg for body fields)", None),
        ("update-workload", "update_workload", ["workload"],
         "update an existing workload (use --arg for body fields)", None),
        ("power", "power", ["workload", "action"],
         "power action: start | stop | restart (workload_id, action)", None),
        # Files & console
        ("list-files", "list_files", ["path"],
         "list files at a path inside the workload", "workload"),
        ("read-file", "read_file", ["path"],
         "read a file from the workload", "workload"),
        ("write-file", "write_file", ["path"],
         "write a file to the workload (use --arg content=...)", "workload"),
        ("edit-file", "edit_file", ["path"],
         "edit a file via the MCP edit primitive (use --arg for edits)",
         "workload"),
        ("move-file", "move_file", ["path"],
         "move/rename a file (use --arg to=...)", "workload"),
        ("delete-file", "delete_file", ["path"],
         "delete a file", "workload"),
        ("mkdir", "create_directory", ["path"],
         "create a directory", "workload"),
        ("search-files", "search_files", ["query"],
         "search files by name/glob", "workload"),
        ("read-console", "read_console", [],
         "tail the server console (use --arg lines=N)", "workload"),
        ("run-command", "run_command", ["command"],
         "run a console command on the server (use --arg workload=ID)",
         None),
        # File transfer
        ("file-transfer", "file_transfer", [],
         "file transfer operation (use --arg for source/dest/etc)", None),
        # Experience building
        ("create-experience", "create_experience", [],
         "create an experience (use --arg for body)", None),
        ("engine-docs", "engine_docs", [],
         "fetch engine docs (use --arg for query)", None),
        ("pack-health", "pack_health", [],
         "report on pack health (use --arg workload=ID)", None),
        # Build inspection
        ("list-parts", "list_parts", [],
         "list parts of a build (use --arg)", None),
        ("check-build", "check_build", [],
         "check a build for errors (use --arg)", None),
        ("render-build", "render_build", [],
         "render a build to an image (use --arg)", None),
        ("render-model", "render_model", [],
         "render a model to an image (use --arg)", None),
        # Publishing
        ("make-experience", "make_experience", [],
         "make an experience (use --arg)", None),
        ("publish-experience", "publish_experience", [],
         "publish an experience (use --arg)", None),
        ("set-experience-visibility", "set_experience_visibility", [],
         "set an experience's visibility (use --arg)", None),
        ("list-releases", "list_releases", [],
         "list releases for an experience (use --arg)", None),
        ("rollback-release", "rollback_release", [],
         "rollback to a release (use --arg)", None),
        ("join-info", "join_info", [],
         "fetch join info for an experience (use --arg)", None),
        # In-game sales
        ("list-products", "list_products", [],
         "list in-game products (use --arg workload=ID)", None),
        ("save-product", "save_product", [],
         "save a product (use --arg for body)", None),
        # Backups
        ("list-backups", "list_backups", [],
         "list backups (use --arg workload=ID)", None),
        ("create-backup", "create_backup", [],
         "create a backup (use --arg workload=ID)", None),
        ("restore-backup", "restore_backup", [],
         "restore a backup (use --arg workload=ID backup=ID)", None),
        # Feedback
        ("send-feedback", "send_feedback", [],
         "send feedback to Minefort (use --arg message=...)", None),
    ]

    for name, tool, pos, help_text, _extras in convenience:
        pc2 = sub.add_parser(name, help=help_text)
        for pname in pos:
            pc2.add_argument(pname, metavar=f"<{pname}>")
        # nargs="*" positional carrier we read back in the handler.
        # (We use dest=_positional only when no explicit positional args
        # are declared — for explicit positionals argparse collects them
        # by name, so the handler reads vars(args) directly.)
        if not pos:
            pc2.add_argument("_positional", nargs="*", metavar="<arg>")
            # argparse mangles leading underscore into "_" already; fine.
        pc2.add_argument("--arg", "-a", action="append", default=[],
                         type=_parse_kv_arg, metavar="KEY=VALUE",
                         help="extra tool argument (repeatable)")
        pc2.add_argument("--raw", action="store_true",
                         help="print the raw MCP result envelope as JSON")
        # For aliases with declared positionals we need a custom handler
        # that reads them off `args` by name.
        if pos:

            def _handler(args, _tool=tool, _pos=pos):
                tok = require_token()
                sess = MCPSession(tok["access_token"])
                arguments: dict[str, Any] = {}
                for pname in _pos:
                    val = getattr(args, pname, None)
                    if val is not None:
                        arguments[pname] = _coerce_value(val)
                for k, v in getattr(args, "args", []) or []:
                    arguments[k] = _coerce_value(v)
                result = sess.call_tool(_tool, arguments)
                if getattr(args, "raw", False):
                    print(json.dumps(result, indent=2, sort_keys=True))
                else:
                    print(_format_result(result))
                return EXIT_OK

            pc2.set_defaults(func=_handler)
        else:
            pc2.set_defaults(func=_make_convenience_runner(tool, []))

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return EXIT_USAGE
    try:
        return args.func(args)
    except KeyboardInterrupt:
        _warn("interrupted")
        return EXIT_USAGE


if __name__ == "__main__":
    sys.exit(main())
