"""The goal gate: no work proceeds without a current goal to work against.

Portable, dependency-free (stdlib only). Drop it at `src/goal_gate.py`.

Usage:
    python src/goal_gate.py                 # may work proceed in this repo at all?
    python src/goal_gate.py --task <id>     # may work proceed on THIS task?
    python src/goal_gate.py --quiet         # exit code only

The weekly goal's age is reported on EVERY run, clear or blocked. Between day 7
and day 14 the gate stays clear but says the goal is AGEING and when it will
block — softening the stop without reporting it would just hide staleness.

Exit codes:
    0  CLEAR   — there is a current, measured, unexpired goal
    1  BLOCKED — there is not; the reasons and the permitted actions are printed
    2  usage / unreadable input

Run this before starting work. An agent that starts a task without a clear gate
is choosing work by what is available rather than by what matters — which is the
entire failure this check exists to stop.

THREE THINGS ARE ALWAYS PERMITTED, gate or no gate. Without them the rule
deadlocks: you could not fix the goals file, because fixing it would be work.

  1. Setting or updating the goals themselves, and running the goal review.
  2. Work labelled `keeping-the-lights-on` — security, data loss, something
     broken that used to work, legal or licensing obligations, a forced platform
     change. This genuinely cannot wait for a goal to be set.
  3. Answering the owner. Conversation is not work.

Everything else waits for a goal.
"""

import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GOALS = ROOT / "plan" / "goals.json"
PLAN = ROOT / "plan" / "plan.json"

EXEMPT_GOALS = {"keeping-the-lights-on"}
# A weekly goal is meant to last a week. It is REPORTED as ageing the moment it
# outlives that (owner rule, 2026-07-29: soften the stop, but say so every time),
# and it BLOCKS at twice its intended life, where it can no longer be called
# current by anyone.
WEEK_AGEING_DAYS = 7
WEEK_STALE_DAYS = 14
REQUIRED_MEASURE_FIELDS = ("name", "baseline", "target", "as_of", "source")

PERMITTED = """Permitted right now, and nothing else:
  1. Set or update the goals — edit plan/goals.json, or run the goal review.
  2. keeping-the-lights-on work — security, data loss, breakage, legal, or a
     forced platform change. Label it `"goal": "keeping-the-lights-on"`.
  3. Answering the owner. Conversation is not work."""


def load(path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"{path.name} is invalid JSON: {e}", file=sys.stderr)
        sys.exit(2)


def measure_faults(m, where):
    if not isinstance(m, dict):
        return [f"{where} has no measure — a goal without a number is a wish"]
    faults = []
    missing = [k for k in REQUIRED_MEASURE_FIELDS if m.get(k) in (None, "")]
    if missing:
        faults.append(f"{where} measure is missing {', '.join(missing)}")
    try:
        if float(m["target"]) <= float(m["baseline"]):
            faults.append(
                f"{where} target ({m['target']}) is not above its baseline "
                f"({m['baseline']}) — that goal is already met"
            )
    except (KeyError, TypeError, ValueError):
        pass
    return faults


def week_age(week):
    starts = (week or {}).get("starts")
    if not starts:
        return None, "the weekly goal has no 'starts' date, so it cannot be checked for staleness"
    try:
        return (date.today() - date.fromisoformat(str(starts))).days, None
    except ValueError:
        return None, f"the weekly goal's 'starts' is not a date ({starts!r})"


def gate(goals):
    """Returns (blocked_reasons, week_goal, days_elapsed).

    Ageing is not blocking: between WEEK_AGEING_DAYS and WEEK_STALE_DAYS the gate
    stays clear and `age_note` reports it. That report is not optional — softening
    the stop without saying anything would simply hide the staleness.
    """
    if goals is None:
        return (["there is no plan/goals.json — this project has no goals at all"], None, None)

    reasons = []
    for period in ("month", "week"):
        g = goals.get(period)
        if not g:
            reasons.append(f"no {period} goal is set — the owner sets both")
            continue
        if not g.get("goal"):
            reasons.append(f"the {period} goal has no text")
        reasons.extend(measure_faults(g.get("measure"), f"the {period} goal's"))

    week = goals.get("week") or {}
    age, err = week_age(week) if week else (None, None)
    if week and err:
        reasons.append(err)
    elif age is not None and age > WEEK_STALE_DAYS:
        reasons.append(
            f"the weekly goal started {age} days ago ({week.get('starts')}) — expired. "
            f"A goal older than {WEEK_STALE_DAYS} days is not something to work against."
        )
    return reasons, week, age


def age_note(age):
    """Reported on EVERY run, clear or not. A softened deadline that says nothing
    is just a longer silence."""
    if age is None:
        return "  Age:       unknown — the weekly goal has no 'starts' date."
    if age > WEEK_STALE_DAYS:
        return f"  Age:       {age} days — EXPIRED (blocks at {WEEK_STALE_DAYS})."
    if age > WEEK_AGEING_DAYS:
        left = WEEK_STALE_DAYS - age
        return (f"  Age:       {age} days — AGEING. A weekly goal was meant to last "
                f"{WEEK_AGEING_DAYS} days; this one has outlived that and blocks in "
                f"{left} day{'s' if left != 1 else ''}. Run the goal review.")
    return f"  Age:       day {age + 1} of {WEEK_AGEING_DAYS} — current."


def find_task(plan, tid):
    for t in (plan or {}).get("tasks", []):
        if t.get("id") == tid:
            return t
    return None


def task_faults(task, tid, goals):
    if task is None:
        return [f"there is no task with id {tid!r} in plan/plan.json"]
    goal = task.get("goal")
    if not goal:
        return [f"task {tid!r} names no goal — say which goal it serves, or "
                f"'keeping-the-lights-on' if it honestly serves none"]
    if goal in EXEMPT_GOALS:
        return []
    current = {(goals.get(p) or {}).get("id") for p in ("month", "week")} - {None} if goals else set()
    faults = []
    if current and goal not in current:
        faults.append(f"task {tid!r} serves {goal!r}, which is not a current goal "
                      f"({', '.join(sorted(current))}) — it needs re-justifying")
    if not task.get("justification"):
        faults.append(f"task {tid!r} has no justification — one line naming the measure it moves")
    return faults


def describe(goals, week, age):
    out = []
    w = goals.get("week") or {}
    m = w.get("measure") or {}
    ageing = age is not None and age > WEEK_AGEING_DAYS
    head = "CLEAR (goal is ageing)" if ageing else "CLEAR"
    out.append(f"{head} — work may proceed against {w.get('id', 'the current goal')}.")
    out.append(f"  This week: {w.get('goal', '')}")
    unit = f" {m['unit']}" if m.get("unit") else ""
    if m:
        cur = m.get("current")
        standing = f" (now {cur}{unit})" if cur is not None else " (not measured yet)"
        out.append(f"  Measure:   {m.get('name', '')} — "
                   f"{m.get('baseline')} -> {m.get('target')}{unit}{standing}")
    mo = goals.get("month") or {}
    if mo.get("goal"):
        out.append(f"  Serving:   {mo.get('id', '')} — {mo['goal']}")
    out.append(age_note(age))
    return "\n".join(out)


def main(argv):
    quiet = "--quiet" in argv
    tid = None
    if "--task" in argv:
        i = argv.index("--task")
        if i + 1 >= len(argv):
            print("--task needs a task id", file=sys.stderr)
            return 2
        tid = argv[i + 1]

    goals = load(GOALS)
    reasons, week, age = gate(goals)

    if tid is not None:
        task = find_task(load(PLAN), tid)
        # Exemption 2 outranks the repo gate: keeping-the-lights-on work is
        # permitted even when there is no goal at all. Checking the gate first
        # would block exactly the work that cannot wait for one.
        if task is not None and task.get("goal") in EXEMPT_GOALS:
            if not quiet:
                print(f"CLEAR — {tid!r} is keeping-the-lights-on work, permitted with or "
                      f"without a current goal.")
                if reasons:
                    print("  Note: this repo's goal gate is BLOCKED for everything else —")
                    for r in reasons:
                        print(f"    · {r}")
            return 0
        reasons = reasons + task_faults(task, tid, goals)

    if reasons:
        if not quiet:
            print("BLOCKED — no current goal to work against."
                  if tid is None else f"BLOCKED — cannot start {tid!r}.")
            print()
            for r in reasons:
                print(f"  · {r}")
            print()
            print(PERMITTED)
        return 1

    if not quiet:
        print(describe(goals, week, age))
        if tid:
            print(f"  Task {tid!r} is justified against a current goal.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
