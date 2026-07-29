#!/usr/bin/env python3
"""Compare each project's installed `.claude/skills/` against this repo's source.

Two copies of a skill always drift eventually — that risk is why this repo
exists. This reports the drift; it never fixes it. Adopting an update is the
project's own decision, in the project's own session
(see conventions/house-rules.md, "This repo never pushes to project repos").

Usage:
    python scripts/skills_drift.py <repo-path>[:<ref>] ...
    python scripts/skills_drift.py --json <repo-path>[:<ref>] ...

`<ref>` defaults to `origin/main` (or `origin/master` when that is the only
one present) so the comparison is against what the project has actually
shipped, not whatever branch a local clone happens to sit on.

Exit status is 0 whether or not drift is found — being behind is a valid
state, not a failure. Use --strict to exit 1 when any project differs.
"""
import hashlib
import json
import os
import subprocess
import sys

SRC_PREFIX = "skills"
INSTALLED_PREFIX = ".claude/skills"
MANUAL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANUAL_REF = "origin/main"


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)


def tree_files(repo, ref, prefix):
    r = git(repo, "ls-tree", "-r", "--name-only", ref, "--", prefix)
    if r.returncode != 0:
        return None
    return sorted(p for p in r.stdout.split("\n") if p.strip())


def blob(repo, ref, path):
    r = git(repo, "show", "%s:%s" % (ref, path))
    return r.stdout if r.returncode == 0 else None


def digest(s):
    return hashlib.sha256(s.encode("utf-8", "replace")).hexdigest()[:12] if s is not None else None


def default_ref(repo):
    for ref in ("origin/main", "origin/master"):
        if git(repo, "rev-parse", "--verify", "--quiet", ref).returncode == 0:
            return ref
    return "HEAD"


def compare(src, repo, ref):
    installed_paths = tree_files(repo, ref, INSTALLED_PREFIX) or []
    installed = {
        p[len(INSTALLED_PREFIX) + 1:]: blob(repo, ref, p) for p in installed_paths
    }

    differs, missing, extra = [], [], []
    identical = 0
    for rel, body in src.items():
        other = installed.get(rel)
        if other is None:
            missing.append(rel)
        elif digest(other) == digest(body):
            identical += 1
        else:
            differs.append(
                {
                    "file": rel,
                    "source_lines": len(body.split("\n")),
                    "installed_lines": len(other.split("\n")),
                }
            )
    for rel in installed:
        if rel not in src:
            extra.append(rel)

    return {
        "repo": repo,
        "ref": ref,
        "installed_count": len(installed),
        "identical": identical,
        "differs": sorted(differs, key=lambda d: d["file"]),
        "missing_from_project": sorted(missing),
        "extra_in_project": sorted(extra),
    }


def main(argv):
    as_json = "--json" in argv
    strict = "--strict" in argv
    targets = [a for a in argv if not a.startswith("-")]
    if not targets:
        print(__doc__.strip())
        return 2

    src_paths = tree_files(MANUAL, MANUAL_REF, SRC_PREFIX)
    if src_paths is None:
        print("cannot read %s:%s — fetch origin first" % (MANUAL_REF, SRC_PREFIX))
        return 2
    src = {p[len(SRC_PREFIX) + 1:]: blob(MANUAL, MANUAL_REF, p) for p in src_paths}

    report = {
        "source_repo": MANUAL,
        "source_ref": MANUAL_REF,
        "source_head": git(MANUAL, "rev-parse", "--short", MANUAL_REF).stdout.strip(),
        "source_last_skills_commit": git(
            MANUAL, "log", "-1", "--format=%h %ad %s", "--date=short",
            MANUAL_REF, "--", SRC_PREFIX,
        ).stdout.strip(),
        "source_file_count": len(src),
        "projects": [],
    }

    for target in targets:
        if ":" in target and not target[1:2] == ":":
            path, ref = target.rsplit(":", 1)
        else:
            path, ref = target, None
        path = os.path.abspath(os.path.expanduser(path))
        if not os.path.isdir(path):
            print("skipping %s — not a directory" % path, file=sys.stderr)
            continue
        git(path, "fetch", "origin", "-q")
        report["projects"].append(compare(src, path, ref or default_ref(path)))

    if as_json:
        print(json.dumps(report, indent=2))
    else:
        print("source: %s @ %s (%d files)" % (report["source_ref"], report["source_head"], report["source_file_count"]))
        print("last change under %s/: %s" % (SRC_PREFIX, report["source_last_skills_commit"]))
        for p in report["projects"]:
            print("\n%s @ %s" % (os.path.basename(p["repo"]), p["ref"]))
            print("  %d installed, %d identical to source" % (p["installed_count"], p["identical"]))
            for d in p["differs"]:
                print("  behind:  %s (source %d lines, installed %d)"
                      % (d["file"], d["source_lines"], d["installed_lines"]))
            for f in p["missing_from_project"]:
                print("  missing: %s" % f)
            for f in p["extra_in_project"]:
                print("  extra:   %s (project's own — not from this repo)" % f)

    drifted = any(p["differs"] or p["missing_from_project"] for p in report["projects"])
    return 1 if (strict and drifted) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
