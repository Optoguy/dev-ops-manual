"""Validate brain frontmatter and maintain brain/INDEX.md.

Portable, dependency-free (stdlib only). Drop it at `src/brain_lint.py` in a repo
whose knowledge base lives under `brain/`.

Usage:
    python src/brain_lint.py                # validate; nonzero exit on problems
    python src/brain_lint.py --write-index  # validate and regenerate brain/INDEX.md

Checks:
- every brain/**/*.md (except _meta/ and INDEX.md) has YAML frontmatter
- knowledge files (brain/knowledge/**) carry: title, tags, sources, last_synced,
  confidence, status
- other brain files carry: title, tags, date, status
- confidence is verified|inferred; status is active|deprecated
- if brain/_meta/drive-manifest.json exists, every knowledge_files path it names
  must exist on disk
- INDEX.md matches what would be regenerated (run --write-index to fix)
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BRAIN = ROOT / "brain"
INDEX = BRAIN / "INDEX.md"
MANIFEST = BRAIN / "_meta" / "drive-manifest.json"

KNOWLEDGE_REQUIRED = {"title", "tags", "sources", "last_synced", "confidence", "status"}
OTHER_REQUIRED = {"title", "tags", "date", "status"}
CONFIDENCE_VALUES = {"verified", "inferred"}
STATUS_VALUES = {"active", "deprecated"}


def parse_frontmatter(path):
    """Return (dict of top-level keys, error string or None)."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return None, "missing frontmatter"
    fm = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fm, None
        m = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if m:
            fm[m.group(1)] = m.group(2).strip()
    return None, "unterminated frontmatter"


def parse_tags(raw):
    return [t.strip() for t in raw.strip("[]").split(",") if t.strip()]


def is_knowledge(path):
    rel = path.relative_to(BRAIN)
    return rel.parts and rel.parts[0] == "knowledge"


def brain_files():
    for path in sorted(BRAIN.rglob("*.md")):
        rel = path.relative_to(BRAIN)
        if rel.parts[0] == "_meta" or rel == Path("INDEX.md"):
            continue
        yield path


def validate():
    errors = []
    for path in brain_files():
        rel = path.relative_to(BRAIN)
        fm, err = parse_frontmatter(path)
        if err:
            errors.append(f"{rel}: {err}")
            continue
        required = KNOWLEDGE_REQUIRED if is_knowledge(path) else OTHER_REQUIRED
        missing = required - set(fm)
        if missing:
            errors.append(f"{rel}: missing frontmatter keys: {', '.join(sorted(missing))}")
        if "confidence" in fm and fm["confidence"] not in CONFIDENCE_VALUES:
            errors.append(f"{rel}: confidence must be verified|inferred (got '{fm['confidence']}')")
        if "status" in fm and fm["status"] not in STATUS_VALUES:
            errors.append(f"{rel}: status must be active|deprecated (got '{fm['status']}')")
        if "tags" in fm and not parse_tags(fm["tags"]):
            errors.append(f"{rel}: tags is empty")

    # Optional: manifest cross-reference.
    if MANIFEST.exists():
        try:
            data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"_meta/drive-manifest.json: invalid JSON ({e})")
        else:
            for entry in _iter_manifest_knowledge_files(data):
                if not (ROOT / entry).exists():
                    errors.append(f"drive-manifest.json references missing file: {entry}")
    return errors


def _iter_manifest_knowledge_files(data):
    """Yield every knowledge_files path mentioned anywhere in the manifest."""
    if isinstance(data, dict):
        for key, value in data.items():
            if key in ("knowledge_files", "knowledge_file"):
                if isinstance(value, str):
                    yield value
                elif isinstance(value, list):
                    yield from (v for v in value if isinstance(v, str))
            else:
                yield from _iter_manifest_knowledge_files(value)
    elif isinstance(data, list):
        for item in data:
            yield from _iter_manifest_knowledge_files(item)


def build_index():
    """Return the INDEX.md text regenerated from the brain on disk."""
    groups = {}
    for path in brain_files():
        rel = path.relative_to(BRAIN)
        fm, err = parse_frontmatter(path)
        title = (fm or {}).get("title") or rel.stem
        tags = ", ".join(parse_tags((fm or {}).get("tags", ""))) if fm else ""
        section = "brain root" if len(rel.parts) == 1 else str(rel.parent).replace("\\", "/") + "/"
        link = f"- [{title}]({rel.as_posix()})" + (f" — {tags}" if tags else "")
        groups.setdefault(section, []).append(link)

    def section_key(name):
        return (0, "") if name == "brain root" else (1, name.lower())

    out = [
        "# Brain index",
        "",
        "One line per brain file. Generated — do not edit by hand; regenerate with",
        "`python src/brain_lint.py --write-index`.",
        "",
    ]
    for section in sorted(groups, key=section_key):
        out.append(f"## {section}")
        out.extend(sorted(groups[section], key=str.lower))
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def main():
    if not BRAIN.exists():
        print(f"no brain/ directory at {BRAIN} — nothing to lint")
        return 0

    write = "--write-index" in sys.argv[1:]
    errors = validate()

    if write:
        INDEX.write_text(build_index(), encoding="utf-8")
        print(f"wrote {INDEX.relative_to(ROOT)}")
    elif INDEX.exists():
        if INDEX.read_text(encoding="utf-8") != build_index():
            errors.append("brain/INDEX.md is stale — run: python src/brain_lint.py --write-index")
    else:
        errors.append("brain/INDEX.md missing — run: python src/brain_lint.py --write-index")

    if errors:
        print(f"\n{len(errors)} problem(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("brain lint: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
