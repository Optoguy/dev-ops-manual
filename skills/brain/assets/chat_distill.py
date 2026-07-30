"""Distil a chat transcript into a durable, portable markdown digest.

Portable, dependency-free (stdlib only). Drop it at `src/chat_distill.py`.

Usage:
    python src/chat_distill.py <transcript.jsonl> [--out docs/history/<date>.md]
    python src/chat_distill.py <transcript.jsonl> --since 2026-07-28
    python src/chat_distill.py --find                 # locate transcripts on this machine
    python src/chat_distill.py <transcript.jsonl> --stats

WHY THIS EXISTS. A chat transcript is the only complete record of *why* a project
looks the way it does — the rejected options, the corrections, the owner's exact
words. The repository keeps conclusions; the chat keeps reasoning. And the
transcript lives in an ephemeral container: when the session's container is
reclaimed, it is gone. Compaction is the nearer threat — a long session's own
memory of week one is a summary of a summary, while the file on disk is complete.

WHAT IT DOES. Mechanical extraction only, no judgment:

  - keeps **owner turns** (the highest-value, lowest-volume signal) and the
    assistant's **prose replies**;
  - drops tool calls and tool results, which are the bulk and are reconstructable
    from git anyway;
  - drops harness noise — interrupt markers, "continue from where you left off",
    system reminders, local command echoes — and collapses duplicates;
  - separates **scheduled firings** (Routine prompts) from genuine owner turns, so
    a nightly prompt repeated twenty times does not read as twenty decisions;
  - redacts anything secret-shaped before it can reach a commit.

Deciding what of this is *durable knowledge* is the reading agent's job — see the
`brain` skill. This produces the raw material, in a format that outlives the
platform that made it.

SAFETY. A transcript contains everything that was ever pasted into the chat,
including things that should never be committed. `redact()` masks common secret
shapes, and the digest is intended for review before it lands. **Never commit a
raw transcript.** The digest is the artefact; the JSONL is not.
"""

import json
import os
import re
import sys
from datetime import date

# Harness chatter that carries no decision.
NOISE = re.compile(
    r"^(\[Request interrupted"
    r"|Continue from where you left off"
    r"|No response requested"
    r"|<system-reminder"
    r"|<local-command"
    r"|<command-"
    r"|Caveat: The messages below)",
    re.I,
)

# A scheduled prompt fires the same long text repeatedly; it is not a new decision.
SCHEDULED_HINTS = (
    "night shift time", "run the /fleet-audit", "run the /method-scan",
    "daily traffic report", "run the traffic report",
)

# Secret shapes. Deliberately broad: a false positive costs a masked string, a
# false negative commits a credential.
SECRET_PATTERNS = [
    (re.compile(r"\b(sk-[A-Za-z0-9_\-]{16,})"), "sk-REDACTED"),
    (re.compile(r"\b(gh[pousr]_[A-Za-z0-9]{16,})"), "gh_REDACTED"),
    (re.compile(r"\b(AIza[0-9A-Za-z_\-]{20,})"), "AIza-REDACTED"),
    (re.compile(r"\b(AKIA[0-9A-Z]{12,})"), "AKIA-REDACTED"),
    (re.compile(r"\b(eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,})"), "jwt-REDACTED"),
    (re.compile(r"(?i)\b(api[_\-]?key|secret|password|token)\s*[=:]\s*['\"]?([^\s'\"]{12,})"),
     r"\1=REDACTED"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----"),
     "-----REDACTED PRIVATE KEY-----"),
]


def redact(text):
    for pattern, repl in SECRET_PATTERNS:
        text = pattern.sub(repl, text)
    return text


def find_transcripts():
    """Where transcripts live on this machine. Platform-specific by nature — the
    fallback for another platform is a reader for its own history format."""
    roots = [
        os.path.expanduser("~/.claude/projects"),
        os.path.expanduser("~/.config/claude/projects"),
    ]
    found = []
    for root in roots:
        if not os.path.isdir(root):
            continue
        for dirpath, _, filenames in os.walk(root):
            for fn in filenames:
                if fn.endswith(".jsonl"):
                    p = os.path.join(dirpath, fn)
                    found.append((p, os.path.getsize(p), os.path.getmtime(p)))
    return sorted(found, key=lambda t: -t[2])


def text_of(content):
    """Message text, or "" when the message is a tool call or tool result."""
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    if any(isinstance(b, dict) and b.get("type") == "tool_result" for b in content):
        return ""
    return "\n".join(b.get("text", "") for b in content
                     if isinstance(b, dict) and b.get("type") == "text")


def parse(path, since=None):
    owner, assistant, scheduled = [], [], []
    tool_calls = 0
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        msg = rec.get("message")
        if not isinstance(msg, dict):
            continue
        day = (rec.get("timestamp") or "")[:10]
        if since and day and day < since:
            continue
        role, content = msg.get("role"), msg.get("content")

        if role == "assistant" and isinstance(content, list):
            tool_calls += sum(1 for b in content
                              if isinstance(b, dict) and b.get("type") == "tool_use")

        body = text_of(content).strip()
        if not body or NOISE.match(body):
            continue
        entry = (day, redact(body))
        if role == "user":
            low = body[:300].lower()
            (scheduled if any(h in low for h in SCHEDULED_HINTS) else owner).append(entry)
        elif role == "assistant":
            assistant.append(entry)

    def dedupe(seq):
        out = []
        for item in seq:
            if not out or out[-1][1] != item[1]:
                out.append(item)
        return out

    return dedupe(owner), dedupe(assistant), dedupe(scheduled), tool_calls


def digest(path, owner, assistant, scheduled, tool_calls, since=None):
    days = sorted({d for d, _ in owner + assistant if d})
    span = f"{days[0]} to {days[-1]}" if days else "unknown"
    chars = sum(len(t) for _, t in owner)
    out = [
        f"# Chat history digest — {span}",
        "",
        f"Distilled {date.today().isoformat()} from `{os.path.basename(path)}`"
        + (f", filtered to {since} onward" if since else "") + ".",
        "",
        "**This is a derived artefact.** The transcript it came from lives in an "
        "ephemeral container and will not survive it. Secret-shaped strings are "
        "masked, but **review before trusting it**, and never commit the raw "
        "transcript.",
        "",
        "| | |",
        "|---|---|",
        f"| Owner turns | {len(owner)} |",
        f"| Assistant replies | {len(assistant)} |",
        f"| Scheduled firings | {len(scheduled)} (separated — a repeated prompt is not a decision) |",
        f"| Tool calls discarded | {tool_calls} (reconstructable from git) |",
        f"| Owner text kept | {chars:,} characters |",
        "",
        "## What the owner asked for, in order",
        "",
        "The decision record of the project in his own words. Everything else in "
        "this file is downstream of these.",
        "",
    ]
    current = None
    for day, text in owner:
        if day != current:
            out += ["", f"### {day or 'undated'}", ""]
            current = day
        flat = " ".join(text.split())
        out.append(f"- {flat}" if len(flat) < 400 else "- " + flat[:400] + " …")

    if scheduled:
        out += ["", "## Scheduled firings", "",
                "Kept as a count per day rather than in full — the prompt text is in "
                "the Routine, not here.", ""]
        per = {}
        for day, _ in scheduled:
            per[day] = per.get(day, 0) + 1
        for day in sorted(per):
            out.append(f"- {day}: {per[day]}")

    out += ["", "## Assistant replies", "",
            "Kept for the reasoning and the findings, which are the part not "
            "recoverable from the diff.", ""]
    current = None
    for day, text in assistant:
        if day != current:
            out += ["", f"### {day or 'undated'}", ""]
            current = day
        flat = " ".join(text.split())
        out.append(f"- {flat[:300]}" + (" …" if len(flat) > 300 else ""))
    return "\n".join(out) + "\n"


def main(argv):
    if "--find" in argv:
        rows = find_transcripts()
        if not rows:
            print("no transcripts found — this platform may keep history elsewhere")
            return 1
        print("%-72s %10s" % ("TRANSCRIPT", "SIZE"))
        for p, size, _ in rows:
            print("%-72s %9.1fM" % (p[-72:], size / 1e6))
        return 0

    paths = [a for a in argv if not a.startswith("-")]
    if not paths:
        print(__doc__.strip())
        return 2
    path = paths[0]
    if not os.path.isfile(path):
        print("no such transcript: %s" % path, file=sys.stderr)
        return 2

    since = None
    if "--since" in argv:
        i = argv.index("--since")
        if i + 1 < len(argv):
            since = argv[i + 1]

    owner, assistant, scheduled, tool_calls = parse(path, since)

    if "--stats" in argv:
        chars = sum(len(t) for _, t in owner)
        print("owner turns:        %d" % len(owner))
        print("assistant replies:  %d" % len(assistant))
        print("scheduled firings:  %d" % len(scheduled))
        print("tool calls dropped: %d" % tool_calls)
        print("owner text:         %d chars (~%d tokens)" % (chars, chars // 4))
        return 0

    text = digest(path, owner, assistant, scheduled, tool_calls, since)
    out = None
    if "--out" in argv:
        i = argv.index("--out")
        if i + 1 < len(argv):
            out = argv[i + 1]
    if out:
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        open(out, "w", encoding="utf-8").write(text)
        print("wrote %s (%d bytes)" % (out, len(text)))
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
