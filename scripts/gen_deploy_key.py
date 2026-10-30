#!/usr/bin/env python3
"""Generate a fresh Ed25519 deploy keypair for citadel-docs sync.

Writes:
  /home/z/my-project/.secrets/id_ed25519      (private, mode 600)
  /home/z/my-project/.secrets/id_ed25519.pub  (public,  mode 644)

Both paths are under .secrets/, which is gitignored — so neither half
can ever leak to GitHub via a stray `git add`.

Ed25519 is generated via the `cryptography` library (a paramiko
dependency, already installed) using standard OpenSSH-format
serialization. The script verifies that paramiko can load the key back
after writing — that proves scripts/git_ssh.py will be able to use it
for fetch/push.

Idempotent: refuses to overwrite an existing private key. Delete the
file first if you want a fresh keypair.
"""
import os
import sys

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
)
import paramiko  # for round-trip verification

SECRETS_DIR = "/home/z/my-project/.secrets"
# Optional argv[1] selects the key slug (default "id" -> id_ed25519, the
# citadel-docs sync key). A second repo needs its own deploy key — GitHub
# allows a key to be a deploy key of only ONE repo — e.g.:
#   python3 gen_deploy_key.py onix_repo
# -> .secrets/onix_repo_ed25519 (+ .pub)
SLUG = (len(sys.argv) > 1 and sys.argv[1]) or "id"
PRIV_PATH = os.path.join(SECRETS_DIR, f"{SLUG}_ed25519")
PUB_PATH = os.path.join(SECRETS_DIR, f"{SLUG}_ed25519.pub")
COMMENT = f"{SLUG}-sync@container"


def main() -> int:
    if os.path.exists(PRIV_PATH):
        print(f"[keygen] refusing to overwrite existing private key at {PRIV_PATH}")
        print("[keygen] delete it first if you genuinely want a fresh keypair.")
        return 1

    os.makedirs(SECRETS_DIR, exist_ok=True)
    os.chmod(SECRETS_DIR, 0o700)

    # Generate Ed25519 keypair and serialize in standard OpenSSH format.
    private_key = Ed25519PrivateKey.generate()
    priv_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,  # OpenSSH priv format is PEM-wrapped
        format=serialization.PrivateFormat.OpenSSH,
        encryption_algorithm=serialization.NoEncryption(),
    )
    with open(PRIV_PATH, "wb") as f:
        f.write(priv_pem)
    os.chmod(PRIV_PATH, 0o600)

    # Public key in authorized_keys format: "ssh-ed25519 <b64> <comment>"
    pub_bytes = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.OpenSSH,
        format=serialization.PublicFormat.OpenSSH,
    )
    # cryptography returns "ssh-ed25519 <b64>" with no comment; add ours.
    pub_line = pub_bytes.decode("ascii").strip() + " " + COMMENT
    with open(PUB_PATH, "w") as f:
        f.write(pub_line + "\n")
    os.chmod(PUB_PATH, 0o644)

    # Round-trip: prove paramiko can load the key we just wrote. If this
    # fails, sync will fail too — better to know now.
    try:
        paramiko.Ed25519Key.from_private_key_file(PRIV_PATH)
    except Exception as e:
        print(f"[keygen] round-trip FAILED — paramiko cannot load the key: {e}")
        return 1

    print("[keygen] generated fresh Ed25519 deploy keypair (round-trip verified):")
    print(f"  private: {PRIV_PATH}  (mode 600, gitignored, stays in container)")
    print(f"  public:  {PUB_PATH}")
    print()
    print("=== PUBLIC KEY — register this on GitHub as a deploy key ===")
    print(pub_line)
    print("=== END PUBLIC KEY ===")
    print()
    # Repo-aware setup instructions. The slug names the key; map the two
    # known slugs to their repos, and keep the citadel-docs default for
    # bare "id".
    repos = {
        "id": ("citadel-docs", "RohanDaCoder/citadel-docs"),
        "onix_repo": ("OnixMinigames", "RohanDaCoder/OnixMinigames"),
    }
    repo_label, repo_path = repos.get(
        SLUG, (SLUG, f"<owner>/{SLUG}")
    )
    print("GitHub setup:")
    print(f"  1. https://github.com/{repo_path}/settings/keys/new")
    print(f"  2. Title: {SLUG}-sync")
    print("  3. Key: paste the single public-key line above")
    print("  4. CHECK 'Allow write access' (required for push)")
    print("  5. Add key")
    print()
    print(f"Then clone {repo_label} with:")
    print(
        f"  GIT_SSH_COMMAND='python3 {os.path.abspath(__file__).replace('gen_deploy_key.py', 'git_ssh.py')} -i {PRIV_PATH}' \\\n"
        f"    git clone git@github.com:{repo_path}.git"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
