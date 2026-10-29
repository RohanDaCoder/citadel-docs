#!/usr/bin/env python3
"""Generate an ed25519 deploy keypair for git SSH pushes.

The container has no ssh-keygen binary, so we use paramiko.
Keys land in ~/.ssh/id_ed25519(.pub). The public key is printed
so it can be added as a GitHub deploy key (with write access).
"""
import os
import sys

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

SSH_DIR = os.path.expanduser("~/.ssh")
PRIV = os.path.join(SSH_DIR, "id_ed25519")
PUB = PRIV + ".pub"
COMMENT = "citadel-wiki-container"


def main() -> int:
    if os.path.exists(PRIV):
        print(f"key already exists: {PRIV}")
        with open(PUB) as fh:
            print(fh.read(), end="")
        return 0

    os.makedirs(SSH_DIR, mode=0o700, exist_ok=True)
    key = Ed25519PrivateKey.generate()
    priv_pem = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.OpenSSH,
        serialization.NoEncryption(),
    )
    with open(PRIV, "wb") as fh:
        fh.write(priv_pem)
    os.chmod(PRIV, 0o600)

    pub_bytes = key.public_key().public_bytes(
        serialization.Encoding.OpenSSH,
        serialization.PublicFormat.OpenSSH,
    )
    pub_line = pub_bytes.decode() + " " + COMMENT + "\n"
    with open(PUB, "w") as fh:
        fh.write(pub_line)
    os.chmod(PUB, 0o644)

    print("generated:", PRIV)
    print()
    print("=== PUBLIC KEY (add as GitHub deploy key with write access) ===")
    print(pub_line, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
