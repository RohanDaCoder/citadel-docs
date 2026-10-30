#!/usr/bin/env python3
"""Keep the local citadel-docs repo in sync with its GitHub remote.

Pipeline (idempotent and safe to run at any time):

    fetch -> integrate (ff-only first, rebase if diverged) -> push

TRANSPORT RESILIENCE (2026-10-30). Container recycles can wipe .secrets/
— the deploy key's private half is unrecoverable from GitHub (only the
public half is stored there), so the sync no longer depends on it for
the fetch side at all:

  * Fetch: anonymous HTTPS first. The repo is public, so this needs no
    credential whatsoever and always works. SSH is the fallback (for a
    private repo or blocked HTTPS) — and git_ssh.py auto-generates a
    fresh keypair when the key file is missing.
  * Push: a GitHub token first, SSH second.
      Token lookup order: `.git/config` `sync.githubtoken` (survives
      container recycles — .git/ demonstrably persists while .secrets/
      does not) > `.secrets/github_token` > `$GITHUB_TOKEN`/`$GH_TOKEN`.
      The token is passed via a throwaway credential helper and is never
      printed. SSH push uses the auto-generated deploy key (works once
      its .pub is registered on the repo with write access).

Integration rules, comparing local HEAD with origin/<branch>:
  * equal            -> nothing to do
  * remote ahead     -> fast-forward local (pulls remote-side edits,
                        e.g. changes made through the GitHub web UI)
  * local ahead      -> push local commits
  * diverged         -> rebase local (unpushed) commits onto origin/<branch>,
                        then push; on conflict, stop and report — never
                        force anything or drop commits

Used by .githooks/post-commit after every commit, and by the periodic
cron sync task so remote changes flow back even when nobody commits.

Guards: skips runs while a rebase/merge/cherry-pick is in progress and
on detached HEAD. Exits 0 on success/nothing-to-do, 1 on failure.
"""
import os
import re
import subprocess
import sys

REPO = "/home/z/my-project"
FALLBACK_URL = "git@github.com:RohanDaCoder/citadel-docs.git"


def env():
    e = dict(os.environ)
    # the container has no openssh-client; route through the paramiko transport
    wrapper = os.path.join(REPO, "scripts", "git_ssh.py")
    if os.path.exists(wrapper):
        e["GIT_SSH_COMMAND"] = f"python3 {wrapper}"
    # never hang waiting for a password prompt (headless cron)
    e["GIT_TERMINAL_PROMPT"] = "0"
    return e


def git(*args):
    return subprocess.run(
        ["git", "-C", REPO, *args],
        capture_output=True,
        text=True,
        env=env(),
    )


def out(r):
    return (r.stdout + r.stderr).strip()


def ssh_to_https(url):
    """git@github.com:USER/REPO.git (or ssh:// form) -> https://github.com/USER/REPO.git"""
    m = re.match(r"^git@([^:/]+):(.+?)(?:\.git)?/?$", url)
    if m:
        return f"https://{m.group(1)}/{m.group(2)}.git"
    m = re.match(r"^ssh://git@([^/]+)/(.+?)(?:\.git)?/?$", url)
    if m:
        return f"https://{m.group(1)}/{m.group(2)}.git"
    if url.startswith("https://"):
        return url if url.endswith(".git") else url.rstrip("/") + ".git"
    return url


def https_to_ssh(url):
    """https://github.com/USER/REPO.git -> git@github.com:USER/REPO.git"""
    m = re.match(r"^https://([^/]+)/(.+?)(?:\.git)?/?$", url)
    if m:
        return f"git@{m.group(1)}:{m.group(2)}.git"
    return url


def get_push_token():
    """Push credential lookup. Never printed by the caller.

    Order: `.git/config` sync.githubtoken (durable across container
    recycles) > `.secrets/github_token` (wiped by recycles, convenience)
    > $GITHUB_TOKEN / $GH_TOKEN env.
    """
    r = git("config", "--get", "sync.githubtoken")
    tok = r.stdout.strip() if r.returncode == 0 else ""
    if tok:
        return tok
    try:
        with open(os.path.join(REPO, ".secrets", "github_token")) as f:
            tok = f.read().strip()
        if tok:
            return tok
    except OSError:
        pass
    for var in ("GITHUB_TOKEN", "GH_TOKEN"):
        tok = os.environ.get(var, "").strip()
        if tok:
            return tok
    return None


def push(branch, https_url, ssh_url):
    """Push HEAD to the remote branch. Token-over-HTTPS first, SSH second.

    Returns (ok, transport, error_text). The token, when used, is fed to
    git through a single-run credential helper so it never appears in
    argv-derived URLs, error messages, or status output.
    """
    token = get_push_token()
    token_err = ""
    if token:
        if not re.fullmatch(r"[A-Za-z0-9_\-]+", token):
            token_err = (
                "token contains unexpected characters; refusing to pass "
                "it to a shell credential helper"
            )
        else:
            helper = (
                "!f() { echo username=x-access-token; "
                f"echo password={token}; }}; f"
            )
            r = git(
                "-c", f"credential.helper={helper}",
                "push", https_url, f"HEAD:refs/heads/{branch}",
            )
            if r.returncode == 0:
                return True, "https+token", ""
            token_err = out(r)

    # SSH path — the paramiko wrapper auto-generates the keypair when the
    # key file is missing, so this always gets as far as GitHub's auth.
    r = git("push", ssh_url, f"HEAD:refs/heads/{branch}")
    if r.returncode == 0:
        return True, "ssh", ""
    err = out(r)
    if token_err:
        err = f"token push failed: {token_err}\nssh push failed: {err}"
    return False, "", err


def main():
    # never interfere with an unfinished operation
    for marker in ("rebase-merge", "rebase-apply", "MERGE_HEAD", "CHERRY_PICK_HEAD"):
        if os.path.exists(os.path.join(REPO, ".git", marker)):
            print(f"[sync] {marker} in progress — skipping this run")
            return 0
    if git("symbolic-ref", "-q", "HEAD").returncode != 0:
        print("[sync] detached HEAD — nothing to do")
        return 0

    has_origin = git("remote", "get-url", "origin").returncode == 0
    fetch_url = (
        git("remote", "get-url", "origin").stdout.strip()
        if has_origin else FALLBACK_URL
    )
    https_url = ssh_to_https(fetch_url)
    # The SSH fallback must honour the remote's PUSH url (origin is now
    # https for fetch + git@ for push); fall back to deriving the git@
    # form from the https url when the push url isn't SSH-shaped.
    if has_origin:
        push_url = git("remote", "get-url", "--push", "origin").stdout.strip()
    else:
        push_url = FALLBACK_URL
    if push_url.startswith(("git@", "ssh://")):
        ssh_url = push_url
    else:
        ssh_url = https_to_ssh(ssh_to_https(push_url))
    branch = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()

    # --- remote state discovery: anonymous HTTPS first (public repo — no
    #     credential, immune to .secrets/ wipes), SSH fallback
    r = git("ls-remote", https_url, f"refs/heads/{branch}")
    transport = "https" if r.returncode == 0 else None
    if transport is None and has_origin:
        r = git("ls-remote", ssh_url, f"refs/heads/{branch}")
        if r.returncode == 0:
            transport = "ssh"
    if transport is None:
        print(f"[sync] fetch failed: {out(r)}")
        return 1

    remote_head = None
    for line in r.stdout.splitlines():
        sha, _, ref = line.partition("\t")
        if ref.strip() == f"refs/heads/{branch}":
            remote_head = sha.strip()

    # --- refresh the remote-tracking ref so the comparison below is exact
    if remote_head is not None:
        src = https_url if transport == "https" else ssh_url
        fr = git("fetch", src, f"+refs/heads/{branch}:refs/remotes/origin/{branch}")
        if fr.returncode != 0:
            print(f"[sync] fetch failed: {out(fr)}")
            return 1
    else:
        # branch absent on the remote — drop any stale tracking ref so the
        # create-branch path below fires naturally
        git("update-ref", "-d", f"refs/remotes/origin/{branch}")

    local = git("rev-parse", "HEAD").stdout.strip()

    if remote_head is None:
        ok, used, err = push(branch, https_url, ssh_url)
        if ok:
            print(f"[sync] created remote {branch} at {local[:7]} (via {used})")
            return 0
        print(f"[sync] push failed: {err}")
        return 1

    if local == remote_head:
        print(f"[sync] already in sync at {local[:7]}")
        return 0

    local_behind = git("merge-base", "--is-ancestor", local, remote_head).returncode == 0
    local_ahead = git("merge-base", "--is-ancestor", remote_head, local).returncode == 0

    if local_behind:
        r = git("merge", "--ff-only", f"refs/remotes/origin/{branch}")
        if r.returncode == 0:
            print(
                f"[sync] fast-forwarded {branch}: {local[:7]} -> "
                f"{remote_head[:7]} (fetched via {transport})"
            )
            return 0
        print(f"[sync] fast-forward blocked (dirty tree?): {out(r)}")
        return 1

    if local_ahead:
        ok, used, err = push(branch, https_url, ssh_url)
        if ok:
            print(f"[sync] pushed {local[:7]} -> origin/{branch} (via {used})")
            return 0
        n = git("rev-list", "--count",
                f"refs/remotes/origin/{branch}..HEAD").stdout.strip() or "?"
        print(f"[sync] push blocked ({n} local commit(s) pending): {err}")
        return 1

    # diverged: rebase local commits onto the remote head, then push
    r = git("-c", "rebase.autoStash=true", "rebase", f"refs/remotes/origin/{branch}")
    if r.returncode != 0:
        print(f"[sync] diverged and rebase hit a conflict — manual resolution needed: {out(r)}")
        return 1
    new_head = git("rev-parse", "HEAD").stdout.strip()
    ok, used, err = push(branch, https_url, ssh_url)
    if ok:
        print(
            f"[sync] rebased {local[:7]} -> {new_head[:7]} onto "
            f"{remote_head[:7]} and pushed (via {used})"
        )
        return 0
    print(f"[sync] push after rebase failed: {err}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
