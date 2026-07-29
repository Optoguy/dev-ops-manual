"""Generate a clean goals-and-status page from plan/goals.json + plan/plan.json.

Portable, dependency-free (stdlib only). Drop it at `src/build_goals.py`.

Usage:
    python src/build_goals.py            # writes dashboard/goals.html
    python src/build_goals.py --check    # nonzero if the page is stale

Shows, for the current month goal and the current week goal:
  - the goal, and the measure it is scored on
  - a progress meter: baseline -> current -> target
  - the work serving it, split open / done
  - the history of finished goals with their outcomes

Design notes:
  - The measure's `current` field is optional. When it is absent the page says
    "not measured yet" rather than implying progress — a goals page that fakes a
    number is worse than one that admits it has none.
  - The generated HTML is deterministic: no today-dependent output is baked in.
    Elapsed and remaining days are computed in the browser from the embedded
    ISO dates, so the file only changes when the data changes and `--check`
    keeps meaning "you forgot to rebuild".
"""

import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GOALS = ROOT / "plan" / "goals.json"
PLAN = ROOT / "plan" / "plan.json"
OUT = ROOT / "dashboard" / "goals.html"

EXEMPT_GOALS = {"keeping-the-lights-on"}
PRIORITY_RANK = {"P0": 0, "P1": 1, "P2": 2}
# Status marks carry a word as well as a colour — never colour alone.
OUTCOME = {
    "hit": ("✔", "hit", "good"),
    "missed": ("✕", "missed", "critical"),
    "abandoned": ("—", "abandoned", "muted"),
}


def esc(s):
    return html.escape(str(s if s is not None else ""))


def load(path, what):
    if not path.exists():
        sys.exit(f"no {what} at {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(f"{path.name} is invalid JSON: {e}")


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def progress(m):
    """Fraction of the way from baseline to target, or None if unmeasured."""
    b, t, c = num(m.get("baseline")), num(m.get("target")), num(m.get("current"))
    if b is None or t is None or c is None or t == b:
        return None
    return max(0.0, min(1.0, (c - b) / (t - b)))


def fmt(v, unit):
    if v is None:
        return "—"
    s = f"{v:g}" if isinstance(v, float) else str(v)
    return f"{s} {unit}".strip() if unit else s


def render_meter(m):
    if not isinstance(m, dict):
        return '<p class="unmeasured">No measure on this goal — a goal without a number is a wish.</p>'
    unit = m.get("unit", "")
    frac = progress(m)
    if frac is None:
        bar = ('<div class="meter unmeasured-bar"><div class="track"></div></div>'
               '<p class="unmeasured">Not measured yet — no current value recorded. '
               'The goal review records it.</p>')
    else:
        pct = round(frac * 100)
        bar = (f'<div class="meter"><div class="track">'
               f'<div class="fill" style="width:{pct}%"></div></div>'
               f'<div class="pct">{pct}% of the way</div></div>')
    cells = [
        ("Baseline", fmt(num(m.get("baseline")), unit)),
        ("Now", fmt(num(m.get("current")), unit)),
        ("Target", fmt(num(m.get("target")), unit)),
    ]
    kpis = "".join(
        f'<div class="kpi"><div class="k-l">{esc(l)}</div><div class="k-v">{esc(v)}</div></div>'
        for l, v in cells
    )
    src = []
    if m.get("as_of"):
        src.append(f"baseline as of {esc(m['as_of'])}")
    if m.get("source"):
        src.append(f"source: {esc(m['source'])}")
    return (f'<div class="m-name">{esc(m.get("name", "unnamed measure"))}</div>'
            + bar
            + f'<div class="kpis">{kpis}</div>'
            + (f'<div class="m-src">{" · ".join(src)}</div>' if src else ""))


def render_goal_card(g, kind, tasks):
    if not g:
        return (f'<section class="card empty"><div class="eyebrow">{esc(kind)}</div>'
                f'<h2 class="goal-text">Not set.</h2>'
                f'<p class="unmeasured">The owner sets this. Until it exists, work here '
                f'is being chosen by what is available rather than what matters.</p></section>')
    gid = g.get("id", "")
    meta = [esc(gid)] if gid else []
    if g.get("supports"):
        meta.append(f'supports {esc(g["supports"])}')
    starts = g.get("starts", "")
    clock = (f'<span class="clock" data-starts="{esc(starts)}" data-kind="{esc(kind)}"></span>'
             if starts else "")
    sep = '<span class="sep">·</span>'
    meta_html = sep.join(meta)
    return (f'<section class="card">'
            f'<div class="eyebrow">{esc(kind)}{sep}{meta_html}{clock}</div>'
            f'<h2 class="goal-text">{esc(g.get("goal", "(no goal text)"))}</h2>'
            f'{render_meter(g.get("measure"))}'
            f'{render_work(gid, tasks)}'
            f'</section>')


def render_work(gid, tasks):
    if not gid:
        return ""
    mine = [t for t in tasks if t.get("goal") == gid]
    if not mine:
        return ('<div class="work"><div class="w-h">Work serving this goal</div>'
                '<p class="unmeasured">None. A goal with no work against it will not move.</p></div>')
    open_t = sorted((t for t in mine if t.get("status") != "done"),
                    key=lambda t: PRIORITY_RANK.get(t.get("priority"), 9))
    done_t = [t for t in mine if t.get("status") == "done"]
    rows = "".join(
        f'<li><span class="prio {esc(t.get("priority","P2")).lower()}">{esc(t.get("priority","P2"))}</span>'
        f'<span class="w-title">{esc(t.get("title","(untitled)"))}</span>'
        f'<span class="w-status">{esc(t.get("status","todo"))}</span></li>'
        for t in open_t
    )
    return (f'<div class="work"><div class="w-h">Work serving this goal '
            f'<span class="w-count">{len(open_t)} open · {len(done_t)} done</span></div>'
            + (f'<ul class="w-list">{rows}</ul>' if rows else
               '<p class="unmeasured">All done — nothing open against this goal.</p>')
            + "</div>")


def render_unassigned(tasks, goal_ids):
    open_t = [t for t in tasks if t.get("status") != "done"]
    lights = [t for t in open_t if t.get("goal") in EXEMPT_GOALS]
    orphan = [t for t in open_t if not t.get("goal") or
              (t.get("goal") not in goal_ids and t.get("goal") not in EXEMPT_GOALS)]
    if not lights and not orphan:
        return ""
    blocks = []
    if lights:
        items = "".join(f'<li>{esc(t.get("title","(untitled)"))}</li>' for t in lights)
        blocks.append(f'<div class="w-h">Keeping the lights on '
                      f'<span class="w-count">{len(lights)}</span></div>'
                      f'<p class="note">Serves no goal, and legitimately so — security, breakage, '
                      f'legal, forced platform changes.</p><ul class="w-list plain">{items}</ul>')
    if orphan:
        items = "".join(f'<li>{esc(t.get("title","(untitled)"))}</li>' for t in orphan)
        blocks.append(f'<div class="w-h flag">Serving no current goal '
                      f'<span class="w-count">{len(orphan)}</span></div>'
                      f'<p class="note">Either the goals are wrong or this work can wait. '
                      f'The goal review decides which.</p><ul class="w-list plain">{items}</ul>')
    return f'<section class="card side">{"".join(blocks)}</section>'


def render_history(history):
    if not history:
        return ""
    rows = []
    for h in history:
        mark, word, cls = OUTCOME.get(h.get("outcome", ""), ("?", h.get("outcome", "unknown"), "muted"))
        m = h.get("measure") or {}
        unit = m.get("unit", "")
        final, target = num(m.get("final")), num(m.get("target"))
        rows.append(
            f'<tr><td class="h-id">{esc(h.get("id",""))}</td>'
            f'<td class="h-goal">{esc(h.get("goal",""))}</td>'
            f'<td class="h-num">{esc(fmt(final, unit))} / {esc(fmt(target, unit))}</td>'
            f'<td><span class="outcome {cls}">{mark} {esc(word)}</span></td></tr>'
        )
    return ('<section class="card"><div class="w-h">Finished goals</div>'
            '<p class="note">Append-only. A history with no misses means the targets are set too low.</p>'
            '<table class="hist"><thead><tr><th>Period</th><th>Goal</th>'
            '<th>Final / target</th><th>Outcome</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></section>')


NAV = [
    ("docs/STRATEGY.html", "Strategy"),
    ("docs/BUSINESS-PLAN.html", "Business plan"),
    ("dashboard/goals.html", "Goals"),
    ("dashboard/index.html", "Task plan"),
    ("docs/PLAN.html", "Roadmap"),
]


def render_nav():
    items = []
    for rel, label in NAV:
        if rel == "dashboard/goals.html":
            items.append(f"<span>{esc(label)}</span>")
        elif (ROOT / rel).exists():
            href = rel.split("/", 1)[1] if rel.startswith("dashboard/") else f"../{rel}"
            items.append(f'<a href="{esc(href)}">{esc(label)}</a>')
    return f'<nav class="nav">{"".join(items)}</nav>' if len(items) > 1 else ""


def render(goals, plan):
    tasks = plan.get("tasks", [])
    ids = {(goals.get(p) or {}).get("id") for p in ("month", "week")} - {None}
    return TEMPLATE.format(
        project=esc(goals.get("project", plan.get("project", "Project"))),
        updated=esc(goals.get("updated", "")),
        nav=render_nav(),
        draft=('<p class="draft">DRAFT — ' + esc(goals["note"]) + "</p>") if goals.get("note") else "",
        month=render_goal_card(goals.get("month"), "This month", tasks),
        week=render_goal_card(goals.get("week"), "This week", tasks),
        unassigned=render_unassigned(tasks, ids),
        history=render_history(goals.get("history")),
    )


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{project} — goals and status</title>
<style>
  :root {{
    --bg:#0f1115; --panel:#171a21; --ink:#e6e9ef; --dim:#9aa4b2;
    --line:#2a2f3a; --accent:#4c8dff;
    --p0:#ff5d5d; --p1:#4c8dff; --p2:#8a93a3;
    --good:#3fbf6b; --critical:#ff5d5d; --warning:#f0a92b;
  }}
  @media (prefers-color-scheme: light) {{
    :root {{ --bg:#f4f6fa; --panel:#fff; --ink:#1a1d24; --dim:#5a6472; --line:#e2e6ee; }}
  }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--ink);
    font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }}
  .wrap {{ max-width:860px; margin:0 auto; padding:28px 20px 60px; }}
  header {{ display:flex; flex-wrap:wrap; align-items:baseline; gap:12px; }}
  header h1 {{ font-size:22px; margin:0; }}
  .sub {{ color:var(--dim); font-size:13px; }}
  .nav {{ display:flex; flex-wrap:wrap; gap:8px; margin:14px 0 4px; }}
  .nav a, .nav span {{ font-size:13px; padding:6px 13px; border-radius:20px;
    text-decoration:none; border:1px solid var(--line); color:var(--dim); background:var(--panel); }}
  .nav a:hover {{ border-color:var(--accent); color:var(--accent); }}
  .nav span {{ border-color:var(--accent); color:var(--accent); font-weight:600; }}
  .draft {{ background:var(--panel); border:1px solid var(--warning); border-left-width:3px;
    border-radius:8px; padding:10px 14px; color:var(--dim); font-size:13px; }}
  .card {{ background:var(--panel); border:1px solid var(--line); border-radius:12px;
    padding:20px 22px; margin:16px 0; }}
  .eyebrow {{ font-size:12px; text-transform:uppercase; letter-spacing:.06em; color:var(--dim);
    display:flex; flex-wrap:wrap; gap:7px; align-items:baseline; }}
  .eyebrow .sep {{ opacity:.45; }}
  .clock {{ text-transform:none; letter-spacing:0; }}
  .clock.stale {{ color:var(--critical); font-weight:600; }}
  .goal-text {{ font-size:19px; font-weight:600; margin:8px 0 18px; line-height:1.35; }}
  .card.empty .goal-text {{ color:var(--dim); font-weight:400; }}
  .m-name {{ font-size:13px; color:var(--dim); margin-bottom:8px; }}
  .meter {{ display:flex; align-items:center; gap:12px; }}
  .track {{ flex:1; height:10px; background:var(--bg); border:1px solid var(--line);
    border-radius:6px; overflow:hidden; }}
  .fill {{ height:100%; background:var(--accent); border-radius:0 4px 4px 0; }}
  .unmeasured-bar .track {{ opacity:.5; }}
  .pct {{ font-size:13px; color:var(--dim); font-variant-numeric:tabular-nums; white-space:nowrap; }}
  .unmeasured {{ color:var(--dim); font-size:13px; margin:8px 0 0; }}
  .kpis {{ display:flex; flex-wrap:wrap; gap:26px; margin:16px 0 0; }}
  .k-l {{ font-size:11px; text-transform:uppercase; letter-spacing:.06em; color:var(--dim); }}
  .k-v {{ font-size:20px; font-variant-numeric:tabular-nums; margin-top:2px; }}
  .m-src {{ font-size:12px; color:var(--dim); margin-top:14px; }}
  .work {{ margin-top:20px; padding-top:16px; border-top:1px solid var(--line); }}
  .w-h {{ font-size:13px; font-weight:600; display:flex; flex-wrap:wrap; gap:8px; align-items:baseline; }}
  .w-h.flag {{ color:var(--warning); }}
  .w-count {{ font-weight:400; color:var(--dim); font-size:12px; }}
  .note {{ font-size:12px; color:var(--dim); margin:4px 0 10px; }}
  .w-list {{ list-style:none; padding:0; margin:10px 0 0; }}
  .w-list li {{ display:flex; gap:10px; align-items:baseline; padding:5px 0;
    border-top:1px solid var(--line); font-size:14px; }}
  .w-list.plain li {{ color:var(--dim); }}
  .prio {{ font-size:11px; font-weight:600; padding:1px 7px; border-radius:9px;
    border:1px solid currentColor; }}
  .prio.p0 {{ color:var(--p0); }} .prio.p1 {{ color:var(--p1); }} .prio.p2 {{ color:var(--p2); }}
  .w-title {{ flex:1; }}
  .w-status {{ font-size:12px; color:var(--dim); }}
  .hist {{ width:100%; border-collapse:collapse; margin-top:6px; font-size:13px; }}
  .hist th {{ text-align:left; font-size:11px; text-transform:uppercase; letter-spacing:.06em;
    color:var(--dim); font-weight:600; padding:6px 10px 6px 0; border-bottom:1px solid var(--line); }}
  .hist td {{ padding:8px 10px 8px 0; border-bottom:1px solid var(--line); vertical-align:top; }}
  .h-num {{ font-variant-numeric:tabular-nums; white-space:nowrap; }}
  .outcome {{ white-space:nowrap; font-weight:600; }}
  .outcome.good {{ color:var(--good); }}
  .outcome.critical {{ color:var(--critical); }}
  .outcome.muted {{ color:var(--dim); }}
  footer {{ color:var(--dim); font-size:12px; margin-top:28px; }}
  @media (max-width:560px) {{ .kpis {{ gap:18px; }} .k-v {{ font-size:17px; }} }}
</style>
</head>
<body>
<div class="wrap">
  <header><h1>{project}</h1><span class="sub">goals and status · updated {updated}</span></header>
  {nav}
  {draft}
  {month}
  {week}
  {unassigned}
  {history}
  <footer>Generated by <code>src/build_goals.py</code> — edit <code>plan/goals.json</code>, not this file.
  Elapsed and remaining days are computed in your browser, so this file changes only when the data does.</footer>
</div>
<script>
/* Deterministic file, live clock: the dates are embedded, the arithmetic is not. */
(function () {{
  var DAY = 864e5;
  document.querySelectorAll('.clock').forEach(function (el) {{
    var startsAt = Date.parse(el.dataset.starts + 'T00:00:00Z');
    if (isNaN(startsAt)) return;
    var weekly = /week/i.test(el.dataset.kind || '');
    var span = weekly ? 7 : 30;
    var elapsed = Math.floor((Date.now() - startsAt) / DAY);
    var left = span - elapsed;
    if (elapsed < 0) {{ el.textContent = 'starts in ' + (-elapsed) + 'd'; return; }}
    if (weekly && elapsed > 7) {{
      el.textContent = 'STALE — set ' + elapsed + ' days ago';
      el.className = 'clock stale';
      return;
    }}
    el.textContent = 'day ' + (elapsed + 1) + ' · ' + (left > 0 ? left + 'd left' : 'over');
  }});
}})();
</script>
</body>
</html>
"""


def main():
    goals = load(GOALS, "plan/goals.json")
    plan = load(PLAN, "plan/plan.json")
    text = render(goals, plan)
    if "--check" in sys.argv[1:]:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != text:
            print("dashboard/goals.html is stale — run: python src/build_goals.py")
            return 1
        print("goals page: up to date")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({goals.get('project','')})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
