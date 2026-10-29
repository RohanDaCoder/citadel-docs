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
import sys

import paramiko

DEFAULT_KEY = os.path.expanduser("~/.ssh/id_ed25519")
# ssh.github.com:443 is the firewall-friendly fallback for port 22
FALLBACKS = {22: ("ssh.github.com", 443)}


def parse_args(argv):
    port = 22
    identity = DEFAULT_KEY
    args = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "-p":
            i += 1
            port = int(argv[i])
        elif a == "-i":
            i += 1
            identity = argv[i]
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
