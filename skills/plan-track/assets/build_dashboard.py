"""Generate a self-contained status dashboard from plan/plan.json.

Portable, dependency-free (stdlib only). Drop it at `src/build_dashboard.py`.

Usage:
    python src/build_dashboard.py                 # reads plan/plan.json, writes dashboard/index.html
    python src/build_dashboard.py --check          # fail (nonzero) if the dashboard is stale or the plan is invalid

The plan is the single source of truth — edit plan/plan.json, never the HTML.
Each task carries:
    owner:    "me" | "agent"
    priority: "P0" | "P1" | "P2"        (P0 = must, P1 = strong, P2 = nice)
    status:   "todo" | "in-progress" | "blocked" | "done"
    phase:    optional phase id
    note, blocked_by, done_date: optional
"""

import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / "plan" / "plan.json"
OUT = ROOT / "dashboard" / "index.html"

OWNERS = {"me": "🧑 Your tasks", "agent": "🤖 Agent tasks"}
PRIORITIES = ["P0", "P1", "P2"]
PRIORITY_RANK = {"P0": 0, "P1": 1, "P2": 2}
STATUS_RANK = {"in-progress": 0, "todo": 1, "blocked": 2, "done": 3}
PRIORITY_LABEL = {"P0": "P0 · must", "P1": "P1 · strong", "P2": "P2 · nice"}


def load_plan():
    if not PLAN.exists():
        sys.exit(f"no plan at {PLAN} — create it from plan.example.json")
    try:
        data = json.loads(PLAN.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(f"plan/plan.json is invalid JSON: {e}")
    return data


def validate(data):
    warnings = []
    for i, t in enumerate(data.get("tasks", [])):
        tid = t.get("id", f"#{i}")
        if t.get("owner") not in OWNERS:
            warnings.append(f"task {tid}: owner should be me|agent (got {t.get('owner')!r}) — rendered in its own column, not dropped")
        if t.get("priority") not in PRIORITY_RANK:
            warnings.append(f"task {tid}: priority should be P0|P1|P2 (got {t.get('priority')!r})")
        if t.get("status") not in STATUS_RANK:
            warnings.append(f"task {tid}: status should be todo|in-progress|blocked|done (got {t.get('status')!r})")
    return warnings


def esc(s):
    return html.escape(str(s if s is not None else ""))


def task_sort_key(t):
    return (PRIORITY_RANK.get(t.get("priority"), 9), STATUS_RANK.get(t.get("status"), 9))


def chip(text, cls):
    return f'<span class="chip {cls}">{esc(text)}</span>'


def render_task(t, phase_titles):
    status = t.get("status", "todo")
    prio = t.get("priority", "P2")
    done = status == "done"
    classes = "task" + (" done" if done else "")
    parts = [f'<li class="{classes}">']
    parts.append('<div class="task-head">')
    parts.append(chip(prio, f"prio {esc(prio).lower()}"))
    parts.append(chip(status, f"status {esc(status)}"))
    parts.append(f'<span class="task-title">{esc(t.get("title", "(untitled)"))}</span>')
    parts.append("</div>")
    meta = []
    ph = t.get("phase")
    if ph and ph in phase_titles:
        meta.append(f'<span class="phase-tag">{esc(phase_titles[ph])}</span>')
    if t.get("blocked_by"):
        meta.append(f'<span class="blocked-by">blocked by {esc(", ".join(t["blocked_by"]))}</span>')
    if done and t.get("done_date"):
        meta.append(f'<span class="done-date">done {esc(t["done_date"])}</span>')
    if meta:
        parts.append(f'<div class="task-meta">{"".join(meta)}</div>')
    if t.get("note"):
        parts.append(f'<div class="task-note">{esc(t["note"])}</div>')
    parts.append("</li>")
    return "".join(parts)


def render_owner_column(owner, tasks, phase_titles):
    heading = OWNERS.get(owner, f"👥 {owner.title()}")
    open_tasks = [t for t in tasks if t.get("status") != "done"]
    done_tasks = [t for t in tasks if t.get("status") == "done"]
    out = [f'<section class="col"><h2>{esc(heading)} <span class="count">{len(open_tasks)} open</span></h2>']
    for prio in PRIORITIES:
        group = sorted((t for t in open_tasks if t.get("priority") == prio), key=task_sort_key)
        if not group:
            continue
        out.append(f'<h3 class="prio-head {prio.lower()}">{esc(PRIORITY_LABEL[prio])} <span class="count">{len(group)}</span></h3>')
        out.append('<ul class="tasks">')
        out.extend(render_task(t, phase_titles) for t in group)
        out.append("</ul>")
    if done_tasks:
        out.append(f'<details class="done-block"><summary>{len(done_tasks)} done</summary><ul class="tasks">')
        out.extend(render_task(t, phase_titles) for t in sorted(done_tasks, key=task_sort_key))
        out.append("</ul></details>")
    out.append("</section>")
    return "".join(out)


def render_next_up(tasks, phase_titles):
    open_tasks = sorted((t for t in tasks if t.get("status") != "done"), key=task_sort_key)
    top = open_tasks[:6]
    if not top:
        return '<div class="next-up"><h2>⏭ Next up</h2><p class="empty">Nothing open — everything is done.</p></div>'
    rows = []
    for t in top:
        owner_badge = {"me": "🧑", "agent": "🤖"}.get(t.get("owner"), "👥")
        rows.append(
            f'<li>{chip(t.get("priority","P2"), "prio " + esc(t.get("priority","P2")).lower())}'
            f'<span class="who">{owner_badge}</span>'
            f'<span class="task-title">{esc(t.get("title","(untitled)"))}</span>'
            f'{chip(t.get("status","todo"), "status " + esc(t.get("status","todo")))}</li>'
        )
    return f'<div class="next-up"><h2>⏭ Next up <span class="count">by priority</span></h2><ul class="tasks">{"".join(rows)}</ul></div>'


# The three linked documents every project carries (see house-rules.md).
# Paths are relative to the repo root; the dashboard lives in dashboard/.
TRIO = [
    ("docs/STRATEGY.html", "Strategy"),
    ("docs/BUSINESS-PLAN.html", "Business plan"),
    ("dashboard/index.html", "Task plan"),
    ("docs/PLAN.html", "Roadmap"),
]


def render_nav():
    """Cross-links to the project's strategy and business plan.

    Only emits links whose targets exist, so a project that hasn't written its
    business plan yet shows fewer chips rather than a dead link.
    """
    items = []
    for rel, label in TRIO:
        target = ROOT / rel
        if rel == "dashboard/index.html":
            items.append(f"<span>{esc(label)}</span>")
            continue
        if target.exists():
            items.append(f'<a href="../{rel}">{esc(label)}</a>')
    return f'<nav class="nav">{"".join(items)}</nav>' if len(items) > 1 else ""


def render(data):
    tasks = data.get("tasks", [])
    phase_titles = {p["id"]: p.get("title", p["id"]) for p in data.get("phases", []) if "id" in p}
    total = len(tasks)
    done = sum(1 for t in tasks if t.get("status") == "done")
    pct = round(100 * done / total) if total else 0
    me = [t for t in tasks if t.get("owner") == "me"]
    agent = [t for t in tasks if t.get("owner") == "agent"]
    extra_owners = []
    for t in tasks:
        o = t.get("owner")
        if o not in ("me", "agent") and o not in extra_owners:
            extra_owners.append(o)
    blocked = sum(1 for t in tasks if t.get("status") == "blocked")
    in_prog = sum(1 for t in tasks if t.get("status") == "in-progress")

    def tile(n, label):
        return f'<div class="tile"><div class="n">{n}</div><div class="l">{esc(label)}</div></div>'

    phases_html = ""
    if data.get("phases"):
        rows = []
        for p in data["phases"]:
            rows.append(
                f'<div class="phase"><div class="phase-title">{esc(p.get("title", p.get("id","")))}</div>'
                f'<div class="phase-goal">{esc(p.get("goal",""))}</div>'
                + (f'<div class="phase-deliv">✔ {esc(p["deliverable"])}</div>' if p.get("deliverable") else "")
                + "</div>"
            )
        phases_html = f'<section class="phases"><h2>Phases</h2>{"".join(rows)}</section>'

    return TEMPLATE.format(
        project=esc(data.get("project", "Project")),
        updated=esc(data.get("updated", "")),
        pct=pct,
        done=done,
        total=total,
        tiles=tile(total, "tasks") + tile(done, "done") + tile(in_prog, "in progress")
        + tile(blocked, "blocked") + tile(len(me), "yours") + tile(len(agent), "agent"),
        nav=render_nav(),
        next_up=render_next_up(tasks, phase_titles),
        me_col=render_owner_column("me", me, phase_titles),
        agent_col=render_owner_column("agent", agent, phase_titles)
        + "".join(render_owner_column(o, [t for t in tasks if t.get("owner") == o], phase_titles)
                  for o in extra_owners),
        phases=phases_html,
    )


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{project} — plan</title>
<style>
  :root {{
    --bg:#0f1115; --panel:#171a21; --panel2:#1e222b; --ink:#e6e9ef; --dim:#9aa4b2;
    --line:#2a2f3a; --accent:#4c8dff;
    --p0:#ff5d5d; --p1:#4c8dff; --p2:#8a93a3;
    --todo:#8a93a3; --inprogress:#f0a92b; --blocked:#ff5d5d; --done:#3fbf6b;
  }}
  @media (prefers-color-scheme: light) {{
    :root {{ --bg:#f4f6fa; --panel:#fff; --panel2:#f0f2f7; --ink:#1a1d24; --dim:#5a6472; --line:#e2e6ee; }}
  }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--ink); font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }}
  .wrap {{ max-width:1100px; margin:0 auto; padding:28px 20px 60px; }}
  header {{ display:flex; flex-wrap:wrap; align-items:baseline; gap:12px; margin-bottom:6px; }}
  header h1 {{ font-size:24px; margin:0; }}
  .nav {{ display:flex; flex-wrap:wrap; gap:8px; margin:0 0 18px; }}
  .nav a, .nav span {{ font-size:13px; padding:6px 13px; border-radius:20px;
    text-decoration:none; border:1px solid var(--line); color:var(--muted); background:var(--card); }}
  .nav a:hover {{ border-color:var(--accent); color:var(--accent); }}
  .nav span {{ background:var(--accent-soft, rgba(31,111,74,.12)); border-color:var(--accent);
    color:var(--accent); font-weight:600; }}
  header .updated {{ color:var(--dim); font-size:13px; }}
  .bar {{ height:10px; background:var(--panel2); border-radius:6px; overflow:hidden; margin:14px 0 4px; }}
  .bar > i {{ display:block; height:100%; width:{pct}%; background:var(--done); }}
  .barlabel {{ color:var(--dim); font-size:13px; margin-bottom:18px; }}
  .tiles {{ display:grid; grid-template-columns:repeat(6,1fr); gap:10px; margin-bottom:22px; }}
  .tile {{ background:var(--panel); border:1px solid var(--line); border-radius:10px; padding:12px; text-align:center; }}
  .tile .n {{ font-size:22px; font-weight:700; }}
  .tile .l {{ font-size:12px; color:var(--dim); text-transform:uppercase; letter-spacing:.04em; }}
  .next-up {{ background:var(--panel); border:1px solid var(--line); border-radius:12px; padding:14px 16px; margin-bottom:24px; }}
  .next-up h2, .col h2, .phases h2 {{ font-size:15px; margin:0 0 10px; text-transform:uppercase; letter-spacing:.05em; color:var(--dim); }}
  .cols {{ display:grid; grid-template-columns:1fr 1fr; gap:18px; }}
  @media (max-width:760px) {{ .cols {{ grid-template-columns:1fr; }} .tiles {{ grid-template-columns:repeat(3,1fr); }} }}
  .col {{ background:var(--panel); border:1px solid var(--line); border-radius:12px; padding:16px; }}
  .col h2 {{ display:flex; justify-content:space-between; align-items:center; }}
  .prio-head {{ font-size:12px; margin:14px 0 8px; letter-spacing:.03em; }}
  .prio-head.p0 {{ color:var(--p0); }} .prio-head.p1 {{ color:var(--p1); }} .prio-head.p2 {{ color:var(--p2); }}
  .count {{ color:var(--dim); font-weight:400; font-size:12px; }}
  ul.tasks {{ list-style:none; margin:0; padding:0; }}
  li.task {{ background:var(--panel2); border:1px solid var(--line); border-radius:9px; padding:9px 11px; margin-bottom:8px; }}
  li.task.done {{ opacity:.5; }}
  li.task.done .task-title {{ text-decoration:line-through; }}
  .task-head {{ display:flex; align-items:center; gap:7px; flex-wrap:wrap; }}
  .task-title {{ font-weight:500; }}
  .task-meta {{ margin-top:5px; display:flex; gap:10px; flex-wrap:wrap; font-size:12px; color:var(--dim); }}
  .task-note {{ margin-top:5px; font-size:13px; color:var(--dim); }}
  .chip {{ font-size:11px; font-weight:700; padding:1px 7px; border-radius:20px; letter-spacing:.02em; white-space:nowrap; }}
  .chip.prio.p0 {{ background:var(--p0); color:#fff; }}
  .chip.prio.p1 {{ background:var(--p1); color:#fff; }}
  .chip.prio.p2 {{ background:var(--p2); color:#fff; }}
  .chip.status {{ border:1px solid var(--line); }}
  .chip.status.todo {{ color:var(--todo); }}
  .chip.status.in-progress {{ color:var(--inprogress); border-color:var(--inprogress); }}
  .chip.status.blocked {{ color:var(--blocked); border-color:var(--blocked); }}
  .chip.status.done {{ color:var(--done); border-color:var(--done); }}
  .next-up li {{ display:flex; align-items:center; gap:9px; padding:6px 0; border-bottom:1px solid var(--line); }}
  .next-up li:last-child {{ border-bottom:0; }}
  .next-up .who {{ font-size:15px; }}
  .next-up .task-title {{ flex:1; }}
  .done-block {{ margin-top:14px; }}
  .done-block summary {{ cursor:pointer; color:var(--dim); font-size:13px; }}
  .phases {{ margin-top:26px; }}
  .phase {{ background:var(--panel); border:1px solid var(--line); border-left:3px solid var(--accent); border-radius:8px; padding:11px 14px; margin-bottom:9px; }}
  .phase-title {{ font-weight:600; }}
  .phase-goal {{ color:var(--dim); font-size:13px; margin-top:2px; }}
  .phase-deliv {{ color:var(--done); font-size:13px; margin-top:4px; }}
  footer {{ margin-top:34px; color:var(--dim); font-size:12px; text-align:center; }}
  code {{ background:var(--panel2); padding:1px 5px; border-radius:4px; }}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>{project}</h1>
    <span class="updated">updated {updated}</span>
  </header>
  {nav}
  <div class="bar"><i></i></div>
  <div class="barlabel">{done} of {total} tasks done · {pct}%</div>
  <div class="tiles">{tiles}</div>
  {next_up}
  <div class="cols">{me_col}{agent_col}</div>
  {phases}
  <footer>Generated by <code>src/build_dashboard.py</code> — edit <code>plan/plan.json</code>, not this file.</footer>
</div>
</body>
</html>
"""


def main():
    data = load_plan()
    warnings = validate(data)
    html_text = render(data)

    check = "--check" in sys.argv[1:]
    if check:
        # Owner-vocabulary notes stay warnings (a repo may use its own vocabulary;
        # tasks render in their own columns) — only structural problems fail --check.
        problems = [w for w in warnings if "rendered in its own column" not in w]
        for w in warnings:
            if w not in problems:
                print(f"warning: {w}", file=sys.stderr)
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != html_text:
            problems.append("dashboard/index.html is stale — run: python src/build_dashboard.py")
        if problems:
            print(f"{len(problems)} problem(s):")
            for p in problems:
                print(f"  - {p}")
            return 1
        print("dashboard: up to date")
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html_text, encoding="utf-8")
    for w in warnings:
        print(f"warning: {w}")
    print(f"wrote {OUT.relative_to(ROOT)} ({data.get('project','')}, "
          f"{sum(1 for t in data.get('tasks',[]) if t.get('status')=='done')}/{len(data.get('tasks',[]))} done)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
