#!/usr/bin/env bash
# VOYGR Prospecting - convenience installer for Claude Code.
#
# PREFER THE PLUGIN (auto-updates):
#   /plugin marketplace add voygr-tech/prospecting
#   /plugin install prospecting@prospecting
#
# This script ONLY copies skills/prospecting/SKILL.md into your Claude Code
# skills dir. No network calls, no other side effects.
set -e
SRC="$(cd "$(dirname "$0")" && pwd)"
DEST="${HOME}/.claude/skills/prospecting"
mkdir -p "$DEST"
cp "$SRC/skills/prospecting/SKILL.md" "$DEST/SKILL.md"
echo "Installed: $DEST/SKILL.md"
echo "Next:"
echo "  1) export VOYGR_API_KEY=<your key>   (free trial: https://app.voygr.tech)"
echo "     Already use PlaceCall? Your PLACECALL_API_KEY is the same account key."
echo "  2) start a fresh Claude Code session (skills load at startup)"
echo "  3) ask it to find businesses, e.g. 'find 20 independent jewelers in Austin with owner emails'"
