#!/usr/bin/env python3
"""Minimal 'ssh' command replacement for git, implemented with paramiko.

The container has no openssh-client, so git cannot speak SSH natively.
Git calls this script through GIT_SSH_COMMAND:

    GIT_SSH_COMMAND="python3 /home/z/my-project/scripts/git_ssh.py" \
        git push git@github.com:user/repo.git main

Usage mirrors a subset of the ssh CLI:
    git_ssh.py [-p port] [-i identity] [-o Opt=val ...] [-T] user@host [command]

Only what git needs is implemented: exec a single remote command and pump
stdio bidirectionally (needed for git-upload-pack / git-receive-pack).
Exit status mirrors the remote command's exit status.
"""
import os
import select
import socket
import subprocess
import sys

try:
    import paramiko
except ModuleNotFoundError:
    # Self-bootstrap: the container's venv can lose paramiko (rebuild,
    # pip purge, fresh checkout). Rather than crash and make git print a
    # misleading "Could not read from remote repository", install it on
    # first use. All pip output is forced to stderr so it never pollutes
    # git's stdout protocol channel (which is wired to this process's
    # stdout during fetch/push). Idempotent: when paramiko is already
    # present the try/except never fires, so zero overhead on the hot
    # path.
    sys.stderr.write("git_ssh.py: paramiko missing — auto-installing...\n")
    _r = subprocess.run(
        [sys.executable, "-m", "pip", "install", "--quiet",
         "--disable-pip-version-check", "--no-input", "paramiko"],
        capture_output=True, text=True,
    )
    if _r.returncode != 0:
        sys.stderr.write(
            f"git_ssh.py: auto-install failed (exit {_r.returncode}): "
            f"{(_r.stderr or _r.stdout).strip()}\n"
        )
        sys.exit(255)
    sys.stderr.write("git_ssh.py: paramiko installed, continuing.\n")
    import paramiko  # retry; if this still fails the real ImportError fires

# Where to look for the deploy key, in priority order.
#
# The home directory (~/.ssh/) can be wiped when the container's venv is
# rebuilt (this already happened once, between 14:00 and 16:00 on
# 2026-10-29). /home/z/my-project/ itself survives such wipes, so the
# PRIMARY key location is the in-project, gitignored .secrets/ dir. The
# ~/.ssh/ paths remain as fallbacks for when the home dir is intact.
#
# An explicit GIT_SSH_IDENTITY env var wins over everything, so ops can
# override without editing code.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY_SEARCH_PATHS = [
    os.path.join(PROJECT_ROOT, ".secrets", "id_ed25519"),
    os.path.join(PROJECT_ROOT, ".secrets", "id_rsa"),
    os.path.expanduser("~/.ssh/id_ed25519"),
    os.path.expanduser("~/.ssh/id_rsa"),
]
# ssh.github.com:443 is the firewall-friendly fallback for port 22
FALLBACKS = {22: ("ssh.github.com", 443)}


def resolve_identity(explicit=None):
    """Pick the SSH key file to use.

    Order: explicit -i flag > $GIT_SSH_IDENTITY > first existing entry in
    KEY_SEARCH_PATHS. Returns None if nothing usable is found, in which
    case connect() will fail with a clear, self-documenting message.
    """
    candidates = []
    if explicit:
        candidates.append(explicit)
    env_override = os.environ.get("GIT_SSH_IDENTITY")
    if env_override:
        candidates.append(env_override)
    candidates.extend(KEY_SEARCH_PATHS)
    for path in candidates:
        if path and os.path.exists(path):
            return path
    # Nothing found — return the primary delete-safe path so the failure
    # message tells the user exactly where to drop the key.
    return KEY_SEARCH_PATHS[0]


def parse_args(argv):
    port = 22
    identity = None  # resolved after parsing so -i / env / defaults merge
    explicit_identity = None
    args = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "-p":
            i += 1
            port = int(argv[i])
        elif a == "-i":
            i += 1
            explicit_identity = argv[i]
        elif a == "-o":
            i += 1  # skip -o option values; policy is fixed (auto-add)
        elif a in ("-T", "-G", "-q"):
            pass
        else:
            args.append(a)
        i += 1
    if not args:
        sys.stderr.write("git_ssh.py: destination required\n")
        sys.exit(255)
    dest = args[0]
    command = " ".join(args[1:]) if len(args) > 1 else None
    if "@" in dest:
        user, host = dest.rsplit("@", 1)
    else:
        user, host = "git", dest
    identity = resolve_identity(explicit_identity)
    return user, host, port, identity, command


def connect(user, host, port, identity):
    attempts = [(host, port)]
    fb = FALLBACKS.get(port)
    if fb:
        attempts.append(fb)
    last_err = None
    client = None
    for h, p in attempts:
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            kwargs = dict(
                hostname=h,
                port=p,
                username=user,
                allow_agent=False,
                look_for_keys=False,
                timeout=15,
            )
            if identity and os.path.exists(identity):
                kwargs["key_filename"] = identity
            client.connect(**kwargs)
            return client
        except (paramiko.SSHException, socket.error, OSError) as err:
            last_err = err
            if client:
                client.close()
    sys.stderr.write(f"git_ssh.py: connection failed: {last_err}\n")
    # Distinguish the unrecoverable auth case so the cron relay is
    # self-documenting instead of just echoing "No authentication
    # methods available". Point at the delete-safe primary location so
    # the user knows exactly where to drop the key.
    if identity is None or not os.path.exists(identity):
        primary = KEY_SEARCH_PATHS[0]
        sys.stderr.write(
            f"git_ssh.py: no usable SSH key found. Restore the deploy "
            f"key (the private half registered on the GitHub repo) to:\n"
            f"    {primary}\n"
            f"  (mode 600, owner-owned). ~/.ssh/id_ed25519 is also "
            f"still honored as a fallback. This cannot be auto-recovered.\n"
        )
    sys.exit(255)


def pump(chan):
    """Bidirectionally stream stdio until the remote command exits."""
    stdin_open = True
    while not chan.exit_status_ready():
        rlist = [chan] + ([0] if stdin_open else [])
        r, _, _ = select.select(rlist, [], [], 0.5)
        if chan in r:
            data = chan.recv(65536)
            if data:
                sys.stdout.buffer.write(data)
                sys.stdout.buffer.flush()
        if chan.recv_stderr_ready():
            data = chan.recv_stderr(65536)
            if data:
                sys.stderr.buffer.write(data)
                sys.stderr.buffer.flush()
        if 0 in r:
            data = os.read(0, 65536)
            if data:
                chan.sendall(data)
            else:
                stdin_open = False
                chan.shutdown_write()
    # drain any residual output
    while chan.recv_ready():
        sys.stdout.buffer.write(chan.recv(65536))
        sys.stdout.buffer.flush()
    while chan.recv_stderr_ready():
        sys.stderr.buffer.write(chan.recv_stderr(65536))
        sys.stderr.buffer.flush()
    sys.stdout.buffer.flush()
    sys.stderr.buffer.flush()
    return chan.recv_exit_status()


def main() -> int:
    user, host, port, identity, command = parse_args(sys.argv[1:])
    client = connect(user, host, port, identity)
    try:
        transport = client.get_transport()
        chan = transport.open_session()
        if command:
            chan.exec_command(command)
        else:
            chan.invoke_shell()  # 'ssh -T' style banner check
        return pump(chan)
    finally:
        client.close()


if __name__ == "__main__":
    sys.exit(main())
