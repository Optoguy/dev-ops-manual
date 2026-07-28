#!/usr/bin/env bash
# Install the dev-skills suite into a Claude Code skills directory,
# and optionally the standing preferences into your user-level CLAUDE.md.
#
#   ./install.sh --global               # skills → ~/.claude/skills/
#   ./install.sh --repo /path/to/repo   # skills → <repo>/.claude/skills/
#   ./install.sh --prefs                # standing prefs → ~/.claude/CLAUDE.md
#   ./install.sh --global --prefs       # both (recommended for first-time setup)
#   ./install.sh --global --dry-run     # print what would happen, write nothing
#
# Each skill is a self-contained directory (SKILL.md + optional assets/), so the
# install is just a copy. Existing skills of the same name are overwritten; other
# skills in the target directory are left untouched. --prefs writes an idempotent
# marked block to ~/.claude/CLAUDE.md (button-UI-for-choices + plan/dashboard
# defaults); re-running it replaces the block in place rather than duplicating it.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$ROOT/skills"
SNIPPET="$ROOT/conventions/global-CLAUDE-snippet.md"

TARGET=""
DO_PREFS=0
DRY_RUN=0

while [ $# -gt 0 ]; do
  case "$1" in
    --global) TARGET="$HOME/.claude/skills" ;;
    --repo)
      shift
      [ $# -gt 0 ] || { echo "error: --repo needs a path" >&2; exit 2; }
      TARGET="$1/.claude/skills"
      ;;
    --prefs) DO_PREFS=1 ;;
    --dry-run) DRY_RUN=1 ;;
    -h|--help)
      sed -n '2,15p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *) echo "error: unknown argument '$1'" >&2; exit 2 ;;
  esac
  shift
done

if [ -z "$TARGET" ] && [ "$DO_PREFS" -eq 0 ]; then
  echo "error: nothing to do — pass --global and/or --repo <path> (skills) and/or --prefs" >&2
  echo "       (add --dry-run to preview)" >&2
  exit 2
fi

[ "$DRY_RUN" -eq 1 ] && echo "(dry run — nothing will be written)" && echo

# --- skills ---------------------------------------------------------------
if [ -n "$TARGET" ]; then
  echo "Skills"
  echo "  source: $SRC"
  echo "  target: $TARGET"
  for skill_dir in "$SRC"/*/; do
    name="$(basename "$skill_dir")"
    if [ "$DRY_RUN" -eq 1 ]; then
      echo "  would install: $name"
    else
      mkdir -p "$TARGET"
      rm -rf "${TARGET:?}/$name"
      cp -R "$skill_dir" "$TARGET/$name"
      echo "  installed: $name"
    fi
  done
  echo
fi

# --- standing preferences -------------------------------------------------
if [ "$DO_PREFS" -eq 1 ]; then
  PREFS_FILE="$HOME/.claude/CLAUDE.md"
  echo "Standing preferences"
  echo "  target: $PREFS_FILE"
  if [ "$DRY_RUN" -eq 1 ]; then
    if [ -f "$PREFS_FILE" ] && grep -q "BEGIN dev-skills prefs" "$PREFS_FILE"; then
      echo "  would REPLACE the existing 'dev-skills prefs' block"
    else
      echo "  would APPEND the 'dev-skills prefs' block"
    fi
  else
    mkdir -p "$(dirname "$PREFS_FILE")"
    touch "$PREFS_FILE"
    # Strip any existing block (idempotent), then append a fresh copy.
    awk '
      /<!-- BEGIN dev-skills prefs -->/ {skip=1}
      skip==0 {print}
      /<!-- END dev-skills prefs -->/ {skip=0}
    ' "$PREFS_FILE" > "$PREFS_FILE.tmp"
    # Collapse trailing blank lines, then separate with exactly one.
    printf '\n' >> "$PREFS_FILE.tmp"
    cat "$SNIPPET" >> "$PREFS_FILE.tmp"
    mv "$PREFS_FILE.tmp" "$PREFS_FILE"
    echo "  wrote the 'dev-skills prefs' block"
  fi
  echo
fi

if [ "$DRY_RUN" -eq 1 ]; then
  echo "Dry run complete. Re-run without --dry-run to apply."
else
  echo "Done. Start a new Claude Code session (or /reload) so changes load."
fi
