<!-- BEGIN dev-skills prefs -->
## Standing preferences

These apply in every project unless a repo's own `CLAUDE.md` overrides them.

**Ask with buttons, not prose.** Whenever you put a choice to me — at any point,
not only at the end of a unit of work — present the options as a clickable menu
via the `AskUserQuestion` tool rather than writing them out as free text. Put the
recommended option first, marked "(Recommended)". Reserve free-text questions for
genuinely open-ended asks with no discrete options. When you finish a unit of
work, end with a 2–4 option `AskUserQuestion` menu of concrete next steps (skip
it only when already asking, mid-task, or there's one obvious next action).

**Every project has a plan and a dashboard.** Keep tasks in a single source of
truth (`plan/plan.json`) where each task carries `owner` (`me` | `agent`),
`priority` (`P0` | `P1` | `P2`), and `status`. Generate a status dashboard from
it (`dashboard/index.html`) that shows *my* tasks and *agent* tasks separately,
each ordered by priority, plus a "Next up" band of the highest-priority open
work. Regenerate the dashboard whenever the plan changes; edit the JSON, never
the HTML. Split ownership honestly: agents build, measure, analyze, and draft; I
own anything with a name, a credential, money, or a git push attached. (The
`project-init`, `plan-track`, `brain`, and `decision-log` skills implement all of
this.)
<!-- END dev-skills prefs -->
