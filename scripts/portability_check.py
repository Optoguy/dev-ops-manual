"""Report what in this repo is bound to one AI platform, and whether it is justified.

Portable, dependency-free (stdlib only). Drop it at `scripts/portability_check.py`.

Usage:
    python scripts/portability_check.py                 # scan and report
    python scripts/portability_check.py --strict        # nonzero if anything is unjustified
    python scripts/portability_check.py --json

Owner rule, 2026-07-30: nothing exclusive to one AI platform unless there is a
clear justification. This does not enforce vendor neutrality — it makes lock-in
visible and checks that each instance of it has a written reason and a fallback,
recorded in `conventions/portability.md`.

This file is excluded from its own scan (it defines the patterns, so it matches all
of them). That is a deliberate blind spot: review changes here by eye.

Two things it checks:

  1. **Platform bindings.** Occurrences of known platform-specific identifiers,
     grouped by concept, each matched against the justification table.
  2. **Third-party imports in portable assets.** This one is objective: a script
     that imports something outside the standard library needs that dependency to
     exist wherever the method runs. Always a strict failure.

It reports and never rewrites. New lock-in is a person's decision; the check only
makes sure it is not silent.
"""

import ast
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONVENTION = os.path.join(ROOT, "conventions", "portability.md")

# Concept -> pattern. Grouped by concept rather than by string, because the
# question "is this justified" is about the binding, not each mention of it.
BINDINGS = {
    "skill install path": r"\.claude/skills",
    "auto-read contract file": r"\bCLAUDE\.md\b",
    "personal preferences path": r"~/\.claude",
    "scheduling (Routines)": r"\bRoutines?\b",
    "clickable menus (AskUserQuestion)": r"\bAskUserQuestion\b",
    "model identifiers": r"\bclaude-[a-z0-9.\-]+\b",
    "provider SDK or endpoint": r"\b(anthropic|openai|gemini|api\.anthropic\.com)\b",
}

# Paths whose contents are history, not live method. Bindings recorded in a dated
# decision, report, or chat digest are describing what happened and must not be
# "fixed" — rewriting the record to look portable is worse than the lock-in.
# Matched as path prefixes, so nested locations like docs/history work.
HISTORICAL_DIRS = ("decisions", "reports", os.path.join("docs", "history"))
SCAN_EXT = (".md", ".py", ".sh", ".json", ".yml", ".yaml", ".toml")
SKIP_DIRS = {".git", "__pycache__", "node_modules", "dashboard"}
# This file defines the patterns, so scanning it matches every one of them. Skipped
# by name — a small, deliberate blind spot: real lock-in added INSIDE the checker
# would not be flagged, so review changes to this file by eye.
SELF = "portability_check.py"
# Portable assets: anything a project installs and runs.
PORTABLE_CODE_DIRS = ("scripts", os.path.join("skills",))


def walk_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn == SELF:
                continue
            if fn.endswith(SCAN_EXT) and not fn.endswith(".html"):
                yield os.path.join(dirpath, fn)


def rel(path):
    return os.path.relpath(path, ROOT)


def justified_concepts():
    """Concepts with a row in the convention's justification table."""
    if not os.path.isfile(CONVENTION):
        return set(), False
    text = open(CONVENTION, encoding="utf-8").read()
    found = set()
    for concept, pattern in BINDINGS.items():
        # A concept counts as justified when the convention mentions its pattern
        # inside the platform-bound table (which is the only place fallbacks live).
        if re.search(pattern, text):
            found.add(concept)
    return found, True


def third_party_imports(path):
    try:
        tree = ast.parse(open(path, encoding="utf-8").read())
    except (SyntaxError, UnicodeDecodeError):
        return []
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            mods.add(node.module.split(".")[0])
    std = getattr(sys, "stdlib_module_names", set())
    return sorted(m for m in mods if m not in std and not m.startswith("_"))


def scan():
    hits = {c: {} for c in BINDINGS}
    for path in walk_files():
        r = rel(path)
        if any(r == h or r.startswith(h + os.sep) for h in HISTORICAL_DIRS):
            continue
        try:
            text = open(path, encoding="utf-8").read()
        except UnicodeDecodeError:
            continue
        for concept, pattern in BINDINGS.items():
            n = len(re.findall(pattern, text))
            if n:
                hits[concept][r] = n

    deps = {}
    for path in walk_files():
        if not path.endswith(".py"):
            continue
        r = rel(path)
        if not any(r.startswith(d) for d in PORTABLE_CODE_DIRS):
            continue
        third = third_party_imports(path)
        if third:
            deps[r] = third
    return hits, deps


def main(argv):
    strict = "--strict" in argv
    as_json = "--json" in argv
    hits, deps = scan()
    justified, have_convention = justified_concepts()

    unjustified = [c for c, files in hits.items() if files and c not in justified]
    portable_py = sum(1 for p in walk_files()
                      if p.endswith(".py") and any(rel(p).startswith(d) for d in PORTABLE_CODE_DIRS))

    if as_json:
        print(json.dumps({
            "convention_present": have_convention,
            "bindings": {c: hits[c] for c in hits if hits[c]},
            "unjustified_concepts": unjustified,
            "third_party_imports": deps,
            "portable_python_files": portable_py,
        }, indent=2))
    else:
        if not have_convention:
            print("no conventions/portability.md — every platform binding below is unjustified\n")
        print("PLATFORM BINDINGS (grouped by concept; %s excluded as history)"
              % ", ".join(h.replace(os.sep, "/") for h in HISTORICAL_DIRS))
        for concept in BINDINGS:
            files = hits[concept]
            if not files:
                continue
            total = sum(files.values())
            mark = "justified" if concept in justified else "** NO JUSTIFICATION **"
            print("  %-38s %4d in %2d files   %s" % (concept, total, len(files), mark))
        print()
        print("PORTABLE PYTHON: %d file(s) checked for third-party imports" % portable_py)
        if deps:
            for f, mods in sorted(deps.items()):
                print("  ** %s imports %s — needs a justification or removal" % (f, ", ".join(mods)))
        else:
            print("  all stdlib-only — these run anywhere Python does")
        print()
        if unjustified:
            print("%d concept(s) bound to a platform with no recorded justification." % len(unjustified))
            print("Record each in conventions/portability.md with a reason and a fallback,")
            print("or replace it with the portable version.")
        elif deps:
            print("Bindings are all justified, but a portable asset has a third-party import.")
        else:
            print("Every platform binding has a recorded justification and fallback.")

    return 1 if (strict and (unjustified or deps)) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
