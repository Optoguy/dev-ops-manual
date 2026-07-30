"""Gather the mechanical state of every project, for a cross-project audit.

Portable, dependency-free (stdlib only). Drop it at `scripts/fleet_state.py`.

Usage:
    python scripts/fleet_state.py <repo-path>[:<ref>] ...
    python scripts/fleet_state.py --json <repo-path>[:<ref>] ...

Reads each project from its **default branch** (or an explicit `<ref>`), never
from whatever a local clone happens to be sitting on — a clone parked on a feature
branch would otherwise report that branch's state as the project's.

This collects only what a script can know for certain: goals present and current,
the ladder intact, task counts, tasks with no goal, how long since the last commit.
**It deliberately does not judge.** Open pull requests, stalled work, contradictions
between a repo and its conventions, and the recommendations are the auditing
agent's job — see the `fleet-audit` skill.

Exit status is 0 unless a path is unreadable. Findings are not failures; this is a
reporting tool.
"""

import json
import os
import subprocess
import sys
from datetime import date

WEEK_AGEING_DAYS = 7
WEEK_STALE_DAYS = 14
REQUIRED_MEASURE_FIELDS = ("name", "baseline", "target", "as_of", "source")
REQUIRED_END_FIELDS = ("goal", "why", "success", "horizon", "strategy")
EXEMPT_GOALS = {"keeping-the-lights-on"}


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)


def blob(repo, ref, path):
    r = git(repo, "show", "%s:%s" % (ref, path))
    return r.stdout if r.returncode == 0 else None


def default_ref(repo):
    for ref in ("origin/main", "origin/master"):
        if git(repo, "rev-parse", "--verify", "--quiet", ref).returncode == 0:
            return ref
    return "HEAD"


def days_since(iso):
    try:
        return (date.today() - date.fromisoformat(str(iso))).days
    except (TypeError, ValueError):
        return None


def read_json(repo, ref, path):
    raw = blob(repo, ref, path)
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return "invalid"


def goals_state(goals):
    """What the goals file says, and what is wrong with it."""
    if goals is None:
        return {"present": False, "faults": ["no plan/goals.json"]}
    if goals == "invalid":
        return {"present": True, "faults": ["plan/goals.json is invalid JSON"]}

    faults = []
    end = goals.get("end") or {}
    if not end:
        faults.append("no end goal — nothing above the monthly goal")
    else:
        miss = [k for k in REQUIRED_END_FIELDS if not str(end.get(k) or "").strip()]
        if miss:
            faults.append("end goal missing " + ", ".join(miss))

    month, week = goals.get("month") or {}, goals.get("week") or {}
    if not month:
        faults.append("no monthly goal")
    if not week:
        faults.append("no weekly goal")

    sup = str(month.get("supports") or "").strip().lower()
    if month and sup not in ("end", "end-goal"):
        faults.append('monthly goal does not declare "supports": "end"')
    if week and month.get("id") and str(week.get("supports") or "") != str(month["id"]):
        faults.append("weekly goal does not support the current month")

    for label, g in (("month", month), ("week", week)):
        m = g.get("measure")
        if g and not isinstance(m, dict):
            faults.append(f"{label} goal has no measure")
            continue
        if g:
            miss = [k for k in REQUIRED_MEASURE_FIELDS if m.get(k) in (None, "")]
            if miss:
                faults.append(f"{label} measure missing " + ", ".join(miss))

    age = days_since(week.get("starts")) if week else None
    if age is not None:
        if age > WEEK_STALE_DAYS:
            faults.append(f"weekly goal EXPIRED — {age} days old")
        elif age > WEEK_AGEING_DAYS:
            faults.append(f"weekly goal ageing — {age} days old, blocks in {WEEK_STALE_DAYS - age}")

    end_age = days_since(end.get("reviewed")) if end else None
    return {
        "present": True,
        "faults": faults,
        "end_goal": end.get("goal"),
        "end_reviewed_days": end_age,
        "month_goal": month.get("goal"),
        "month_id": month.get("id"),
        "week_goal": week.get("goal"),
        "week_id": week.get("id"),
        "week_age_days": age,
        "blocked": bool([f for f in faults if "ageing" not in f]),
    }


def plan_state(plan):
    """Task counts, and the tasks that cannot justify themselves."""
    if plan is None:
        return {"present": False,
                "note": "no plan/plan.json — this repo may declare a different task "
                        "source of truth; read its CLAUDE.md"}
    if plan == "invalid":
        return {"present": True, "note": "plan/plan.json is invalid JSON"}
    tasks = plan.get("tasks", [])
    open_t = [t for t in tasks if t.get("status") != "done"]
    return {
        "present": True,
        "total": len(tasks),
        "done": len(tasks) - len(open_t),
        "open": len(open_t),
        "in_progress": sum(1 for t in open_t if t.get("status") == "in-progress"),
        "blocked": sum(1 for t in open_t if t.get("status") == "blocked"),
        "owner_me": sum(1 for t in open_t if t.get("owner") == "me"),
        "owner_agent": sum(1 for t in open_t if t.get("owner") == "agent"),
        "p0_open": sum(1 for t in open_t if t.get("priority") == "P0"),
        "no_goal": [t.get("id") for t in open_t if not t.get("goal")],
        "no_justification": [t.get("id") for t in open_t
                             if t.get("goal") and t["goal"] not in EXEMPT_GOALS
                             and not t.get("justification")],
        "lights_on": [t.get("id") for t in open_t if t.get("goal") in EXEMPT_GOALS],
    }


def history_state(repo, ref):
    """How fresh the project's captured chat history is.

    A transcript lives in the container of the session that made it, so no other
    session can capture it — this is the one thing the fleet view can enforce but
    not perform. Reports the newest period file and how long ago it was touched.
    """
    r = git(repo, "ls-tree", "-r", "--name-only", ref, "--", "docs/history")
    files = sorted(p for p in r.stdout.split("\n") if p.strip().endswith(".md"))
    if not files:
        return {"present": False,
                "note": "no docs/history/ — chat history is not being captured, so it "
                        "dies with the container that holds it"}
    last = git(repo, "log", "-1", "--format=%ad", "--date=short", ref,
               "--", "docs/history").stdout.strip()
    return {"present": True, "periods": len(files), "newest_file": files[-1],
            "last_captured": last, "days_since": days_since(last)}


def collect(path, ref):
    git(path, "fetch", "origin", "-q")
    ref = ref or default_ref(path)
    last = git(path, "log", "-1", "--format=%h|%ad|%s", "--date=short", ref).stdout.strip()
    sha, when, subject = (last.split("|", 2) + ["", "", ""])[:3] if last else ("", "", "")
    pin = ""
    cm = blob(path, ref, "CLAUDE.md") or ""
    for ln in cm.split("\n"):
        low = ln.lower()
        if "dev-ops-manual" in low and ("commit" in low or "pin" in low):
            pin = ln.strip()
            break
    return {
        "name": os.path.basename(os.path.abspath(path)),
        "path": os.path.abspath(path),
        "ref": ref,
        "last_commit": {"sha": sha, "date": when, "subject": subject,
                        "days_ago": days_since(when)},
        "manual_pin_line": pin,
        "history": history_state(path, ref),
        "goals": goals_state(read_json(path, ref, "plan/goals.json")),
        "plan": plan_state(read_json(path, ref, "plan/plan.json")),
    }


def print_text(rows):
    print("%-22s %-14s %-9s %-24s %s" % ("PROJECT", "REF", "GATE", "OPEN TASKS", "LAST COMMIT"))
    for r in rows:
        g = r["goals"]
        gate = "n/a" if not g.get("present") else ("BLOCKED" if g.get("blocked") else "clear")
        pl = r["plan"]
        tasks = ("%d open (%d P0, %d yours)" % (pl["open"], pl["p0_open"], pl["owner_me"])
                 if pl.get("present") and "total" in pl else "—")
        d = r["last_commit"]
        ago = f"{d['days_ago']}d ago" if d.get("days_ago") is not None else "?"
        print("%-22s %-14s %-9s %-24s %s (%s)" % (r["name"][:22], r["ref"][:14], gate, tasks, ago, d["date"]))

    for r in rows:
        print("\n" + r["name"])
        g, pl = r["goals"], r["plan"]
        if g.get("end_goal"):
            print("  end goal:  %s" % g["end_goal"])
            if g.get("end_reviewed_days") is not None:
                print("             confirmed %d days ago" % g["end_reviewed_days"])
        if g.get("month_goal"):
            print("  month %-6s %s" % (g.get("month_id") or "", g["month_goal"]))
        if g.get("week_goal"):
            age = g.get("week_age_days")
            print("  week  %-6s %s%s" % (g.get("week_id") or "", g["week_goal"],
                                         f"  (day {age + 1})" if age is not None else ""))
        for f in g.get("faults", []):
            print("  fault:     %s" % f)
        if pl.get("note"):
            print("  note:      %s" % pl["note"])
        for label, key in (("no goal", "no_goal"), ("no justification", "no_justification")):
            if pl.get(key):
                print("  %s: %s" % (label, ", ".join(pl[key])))
        if pl.get("lights_on"):
            print("  lights-on: %s" % ", ".join(pl["lights_on"]))
        h = r.get("history") or {}
        if not h.get("present"):
            print("  history:   NOT CAPTURED — %s" % h.get("note", ""))
        else:
            d = h.get("days_since")
            flag = "" if d is None or d <= 7 else "  <- STALE"
            print("  history:   %d period(s), last captured %s (%s days ago)%s"
                  % (h["periods"], h.get("last_captured", "?"), d, flag))
        if r.get("manual_pin_line"):
            print("  pinned:    %s" % r["manual_pin_line"])


def main(argv):
    as_json = "--json" in argv
    targets = [a for a in argv if not a.startswith("-")]
    if not targets:
        print(__doc__.strip())
        return 2
    rows = []
    for t in targets:
        path, ref = (t.rsplit(":", 1) if ":" in t and t[1:2] != ":" else (t, None))
        path = os.path.abspath(os.path.expanduser(path))
        if not os.path.isdir(path):
            print("skipping %s — not a directory" % path, file=sys.stderr)
            continue
        rows.append(collect(path, ref))
    if as_json:
        print(json.dumps({"as_of": date.today().isoformat(), "projects": rows}, indent=2))
    else:
        print_text(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
