#!/usr/bin/env bash
# Scrub the DiscordSRV BotToken value from the unpushed commits only
# (range: origin/main..HEAD). Blanks the token value -> "" in every
# commit's tree. Does NOT delete files, does NOT rewrite any pushed
# history (origin/main and earlier stay byte-identical).
#
# Backup of the pre-rewrite branch is auto-saved by filter-branch at
# refs/original/refs/heads/main, and is also recoverable via reflog.
set -euo pipefail
cd /home/z/my-project
export FILTER_BRANCH_SQUELCH_WARNING=1

echo "=== pre-rewrite state ==="
echo "main (pre) = $(git rev-parse main)"
echo "origin/main (untouched target) = $(git rev-parse origin/main)"
echo "commits to rewrite:"
git log --oneline origin/main..HEAD

echo
echo "=== running filter-branch --tree-filter over origin/main..HEAD ==="
git filter-branch -f --tree-filter '
  f="scripts/onixmg_citadel/reference/configs/DiscordSRV_config.yml"
  if [ -f "$f" ]; then
    sed -i "s|BotToken: \"[^\"]*\"|BotToken: \"\"|g" "$f"
  fi
' -- origin/main..HEAD

echo
echo "=== post-rewrite state ==="
echo "main (post) = $(git rev-parse main)"
echo "origin/main (should be unchanged) = $(git rev-parse origin/main)"
echo "commits after rewrite:"
git log --oneline origin/main..HEAD
