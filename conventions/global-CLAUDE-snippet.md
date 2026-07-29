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

**Every project has goals I set, and every suggestion says which one it serves.**
Each project keeps a current monthly goal and a current weekly goal in
`plan/goals.json`, and **I set them** — you draft candidates with the evidence
behind each, I choose. Every goal carries one measure with a baseline, a target,
a date, and a named source; a goal without a number is a wish. Every piece of
work you suggest names the goal it serves and, in one line, the measure it moves
and where that measure stands today — in the task file, in every menu you put to
me, and in the pull request. If work genuinely serves no goal, say so plainly and
label it "keeping the lights on" (security, breakage, legal, a forced platform
change); that answer is fine, and inventing a justification is not. If my weekly
goal is more than seven days old, ask me for a new one before proposing anything
else.

**Write so the next step is obvious.** Lead with what you need from me in plain
words — reasoning after, if at all. No abbreviations (write "pull request", not
"PR"). No internal nicknames from your own analysis. One ask per message. Say
where to click and what will be true afterwards. Short sentences. And say
plainly when there is nothing for me to do.

**End every response with the choices, clearly marked.** Close with a section
headed "Your options" — numbered, plain language, one line each on what happens
if I pick it, the recommended one marked. Two to four options, including the
do-nothing option when it is real. Write the list out even when you also show a
clickable menu. If there is genuinely nothing to decide, say "Nothing for you to
do" instead. Never end with "let me know what you think".
<!-- END dev-skills prefs -->
