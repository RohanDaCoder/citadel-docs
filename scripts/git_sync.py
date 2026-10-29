#!/usr/bin/env python3
"""Keep the local citadel-docs repo in sync with its GitHub remote.

Pipeline (idempotent and safe to run at any time):

    fetch -> integrate (ff-only first, rebase if diverged) -> push

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
    remote = "origin" if has_origin else FALLBACK_URL
    branch = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()

    r = git("fetch", remote)
    if r.returncode != 0:
        print(f"[sync] fetch failed: {out(r)}")
        return 1

    local = git("rev-parse", "HEAD").stdout.strip()

    if not has_origin:
        # push-only mode: a bare URL cannot provide remote-tracking refs
        r = git("push", remote, "HEAD")
        if r.returncode == 0:
            print(f"[sync] pushed {local[:7]} to {remote}")
            return 0
        print(f"[sync] push failed: {out(r)}")
        return 1

    upstream = f"origin/{branch}"
    ru = git("rev-parse", upstream)
    if ru.returncode != 0:
        # remote branch does not exist yet — create it
        r = git("push", remote, f"HEAD:refs/heads/{branch}")
        if r.returncode == 0:
            print(f"[sync] created {remote}/{branch} at {local[:7]}")
            return 0
        print(f"[sync] push failed: {out(r)}")
        return 1
    remote_head = ru.stdout.strip()

    if local == remote_head:
        print(f"[sync] already in sync at {local[:7]}")
        return 0

    local_behind = git("merge-base", "--is-ancestor", local, remote_head).returncode == 0
    local_ahead = git("merge-base", "--is-ancestor", remote_head, local).returncode == 0

    if local_behind:
        r = git("merge", "--ff-only", upstream)
        if r.returncode == 0:
            print(f"[sync] fast-forwarded {branch}: {local[:7]} -> {remote_head[:7]}")
            return 0
        print(f"[sync] fast-forward blocked (dirty tree?): {out(r)}")
        return 1

    if local_ahead:
        r = git("push", remote, "HEAD")
        if r.returncode == 0:
            print(f"[sync] pushed {local[:7]} -> {remote}/{branch}")
            return 0
        print(f"[sync] push failed: {out(r)}")
        return 1

    # diverged: rebase local commits onto the remote head, then push
    r = git("-c", "rebase.autoStash=true", "rebase", upstream)
    if r.returncode != 0:
        print(f"[sync] diverged and rebase hit a conflict — manual resolution needed: {out(r)}")
        return 1
    new_head = git("rev-parse", "HEAD").stdout.strip()
    r = git("push", remote, "HEAD")
    if r.returncode == 0:
        print(f"[sync] rebased {local[:7]} -> {new_head[:7]} onto {remote_head[:7]} and pushed")
        return 0
    print(f"[sync] push after rebase failed: {out(r)}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
