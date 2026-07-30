#!/usr/bin/env python3
"""Render markdown plans and to-do lists to self-contained HTML.

    python scripts/render_docs.py docs/PLAN.md docs/BACKLOG.md
    python scripts/render_docs.py docs/*.md
    python scripts/render_docs.py --check docs/PLAN.md   # nonzero if stale

House rule: every plan or to-do list that exists as markdown also exists as
HTML, so it can be opened and read without a markdown viewer. The markdown is
the source; the HTML is generated — never hand-edit it.

Writes `<name>.html` beside each `<name>.md`. Output is dependency-free and
fully self-contained (inline CSS, no external assets, no JS), so it opens
offline and survives a strict CSP.

No third-party imports — standard library only.
"""
import html
import os
import re
import sys

CSS = """
:root { --bg:#fbfaf7; --panel:#fff; --ink:#1c1b18; --muted:#5f5c55; --faint:#8a8681;
  --line:#e5e1d8; --accent:#1f6f4a; --accent-soft:#e8f3ed; --code:#f4f2ec; }
@media (prefers-color-scheme: dark) {
  :root { --bg:#14150f; --panel:#1b1c16; --ink:#e9e7df; --muted:#a8a49a; --faint:#7d7a72;
    --line:#2c2e25; --accent:#7fc9a1; --accent-soft:#1d2b23; --code:#22241c; } }
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--ink); line-height:1.65;
  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
  -webkit-font-smoothing:antialiased; }
.wrap { max-width:820px; margin:0 auto; padding:34px 22px 70px; }
.src { color:var(--faint); font-size:12px; letter-spacing:.06em; text-transform:uppercase;
  margin-bottom:22px; padding-bottom:12px; border-bottom:1px solid var(--line); }
.nav { display:flex; flex-wrap:wrap; gap:8px; margin-bottom:18px; }
.nav a, .nav span { font-size:13px; padding:6px 13px; border-radius:20px; text-decoration:none;
  border:1px solid var(--line); color:var(--muted); background:var(--panel); }
.nav a:hover { border-color:var(--accent); color:var(--accent); }
.nav span { background:var(--accent-soft); border-color:var(--accent); color:var(--accent);
  font-weight:600; }
h1 { font-size:clamp(24px,4vw,32px); line-height:1.2; margin:0 0 16px; letter-spacing:-.01em; }
h2 { font-size:clamp(18px,2.6vw,22px); margin:34px 0 10px; padding-bottom:6px;
  border-bottom:1px solid var(--line); }
h3 { font-size:16.5px; margin:24px 0 8px; }
h4 { font-size:15px; margin:18px 0 6px; color:var(--muted); }
p { margin:0 0 13px; }
ul, ol { margin:0 0 14px; padding-left:24px; }
li { margin-bottom:5px; }
li::marker { color:var(--faint); }
a { color:var(--accent); }
code { background:var(--code); padding:1.5px 5px; border-radius:4px; font-size:.9em;
  font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; }
pre { background:var(--code); padding:14px 16px; border-radius:9px; overflow-x:auto;
  border:1px solid var(--line); margin:0 0 15px; }
pre code { background:none; padding:0; font-size:13px; }
blockquote { margin:0 0 15px; padding:10px 16px; border-left:3px solid var(--accent);
  background:var(--accent-soft); border-radius:0 8px 8px 0; color:var(--muted); }
blockquote p:last-child { margin-bottom:0; }
.tablewrap { overflow-x:auto; margin:0 0 16px; }
table { border-collapse:collapse; width:100%; font-size:14.5px; background:var(--panel);
  border:1px solid var(--line); border-radius:9px; overflow:hidden; }
th, td { text-align:left; padding:9px 13px; border-bottom:1px solid var(--line);
  vertical-align:top; }
th { background:var(--code); font-weight:650; font-size:13px; letter-spacing:.02em; }
tr:last-child td { border-bottom:none; }
hr { border:none; border-top:1px solid var(--line); margin:28px 0; }
.task { list-style:none; margin-left:-22px; }
.task li { padding-left:26px; position:relative; }
.task li::before { position:absolute; left:0; top:0; font-size:14px; }
.task li.todo::before { content:'\\2610'; color:var(--faint); }
.task li.done::before { content:'\\2611'; color:var(--accent); }
.task li.done { color:var(--muted); }
"""

INLINE = [
    (re.compile(r'`([^`]+)`'), lambda m: "<code>" + html.escape(m.group(1)) + "</code>"),
    (re.compile(r'!\[([^\]]*)\]\(([^)]+)\)'), lambda m: ""),   # images: no external assets
    (re.compile(r'\[([^\]]+)\]\(([^)]+)\)'),
     lambda m: '<a href="%s">%s</a>' % (safe_href(m.group(2)), m.group(1))),
    (re.compile(r'\*\*([^*]+)\*\*'), lambda m: "<strong>%s</strong>" % m.group(1)),
    (re.compile(r'(?<![*\w])\*([^*\n]+)\*(?!\*)'), lambda m: "<em>%s</em>" % m.group(1)),
    (re.compile(r'(?<!\w)_([^_\n]+)_(?!\w)'), lambda m: "<em>%s</em>" % m.group(1)),
    (re.compile(r'~~([^~]+)~~'), lambda m: "<del>%s</del>" % m.group(1)),
]


def safe_href(url):
    """Reject scripting schemes; escape for attribute position."""
    stripped = re.sub(r'[\x00-\x20]', '', url)
    if re.match(r'^(javascript|data|vbscript):', stripped, re.I):
        return "#"
    return html.escape(url, quote=True)


def inline(text):
    out = html.escape(text)
    for pattern, repl in INLINE:
        out = pattern.sub(repl, out)
    return out


def render(md):
    lines = md.replace("\r\n", "\n").split("\n")
    out, i = [], 0
    list_stack = []      # open list tags, innermost last

    def close_lists():
        while list_stack:
            out.append("</%s>" % list_stack.pop())

    while i < len(lines):
        line = lines[i]

        if line.startswith("```"):                              # fenced code
            close_lists()
            i += 1
            buf = []
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i]); i += 1
            i += 1
            out.append("<pre><code>%s</code></pre>" % html.escape("\n".join(buf)))
            continue

        if not line.strip():
            close_lists(); i += 1; continue

        m = re.match(r'^(#{1,6})\s+(.*)$', line)                # heading
        if m:
            close_lists()
            level = min(len(m.group(1)), 4)
            out.append("<h%d>%s</h%d>" % (level, inline(m.group(2).strip()), level))
            i += 1; continue

        if re.match(r'^\s*([-*_])\s*\1\s*\1[\s\1]*$', line):     # horizontal rule
            close_lists(); out.append("<hr>"); i += 1; continue

        if line.lstrip().startswith(">"):                        # blockquote
            close_lists()
            buf = []
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                buf.append(re.sub(r'^\s*>\s?', '', lines[i])); i += 1
            out.append("<blockquote>%s</blockquote>" %
                       "".join("<p>%s</p>" % inline(p) for p in
                               " ".join(buf).split("\n") if p.strip()))
            continue

        if "|" in line and i + 1 < len(lines) and re.match(
                r'^\s*\|?[\s:|-]+\|[\s:|-]*$', lines[i + 1]):    # table
            close_lists()
            def cells(row):
                return [c.strip() for c in row.strip().strip("|").split("|")]
            head = cells(line); i += 2
            rows = []
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                rows.append(cells(lines[i])); i += 1
            thead = "".join("<th>%s</th>" % inline(c) for c in head)
            tbody = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c) for c in r)
                            for r in rows)
            out.append('<div class="tablewrap"><table><thead><tr>%s</tr></thead>'
                       "<tbody>%s</tbody></table></div>" % (thead, tbody))
            continue

        m = re.match(r'^(\s*)([-*+]|\d+[.)])\s+(.*)$', line)     # list item
        if m:
            indent, marker, body = len(m.group(1)), m.group(2), m.group(3)
            ordered = not marker[0] in "-*+"
            depth = indent // 2 + 1
            task = re.match(r'^\[([ xX])\]\s*(.*)$', body)
            while len(list_stack) > depth:
                out.append("</%s>" % list_stack.pop())
            if len(list_stack) < depth:
                tag = "ol" if ordered else "ul"
                cls = ' class="task"' if task else ""
                out.append("<%s%s>" % (tag, cls))
                list_stack.append(tag)
            if task:
                done = task.group(1).lower() == "x"
                out.append('<li class="%s">%s</li>' %
                           ("done" if done else "todo", inline(task.group(2))))
            else:
                out.append("<li>%s</li>" % inline(body))
            i += 1; continue

        close_lists()                                            # paragraph
        buf = []
        while i < len(lines) and lines[i].strip() and not re.match(
                r'^(\s*([-*+]|\d+[.)])\s|#{1,6}\s|>|```)', lines[i]):
            buf.append(lines[i].strip()); i += 1
        if buf:
            out.append("<p>%s</p>" % inline(" ".join(buf)))

    close_lists()
    return "\n".join(out)


# The three linked documents every project carries, plus the narrative plan.
# Each generated page navigates to whichever of these exist — see house-rules.
TRIO = [
    ("docs/STRATEGY.html", "Strategy"),
    ("docs/BUSINESS-PLAN.html", "Business plan"),
    ("dashboard/goals.html", "Goals"),
    ("dashboard/index.html", "Task plan"),
    ("docs/PLAN.html", "Roadmap"),
]


def repo_root(start):
    """Walk up from a file to the repo root (.git, or a plan/ + docs/ pair)."""
    d = os.path.dirname(os.path.abspath(start)) or "."
    while True:
        if (os.path.isdir(os.path.join(d, ".git"))
                or os.path.isdir(os.path.join(d, "plan"))
                or os.path.isdir(os.path.join(d, "dashboard"))):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def nav(md_path, planned=()):
    """Cross-links to the project's strategy / business plan / task plan.

    Emitted only for targets that exist or are being written in this same run
    (`planned`), so a project without a business plan yet simply shows fewer
    links — never a dead one, and never one that depends on render order.
    """
    root = repo_root(md_path)
    if not root:
        return ""
    here = os.path.abspath(md_path[:-3] + ".html")
    items = []
    for rel, label in TRIO:
        target = os.path.join(root, rel)
        if not (os.path.exists(target) or os.path.abspath(target) in planned):
            continue
        if os.path.abspath(target) == here:
            items.append("<span>%s</span>" % html.escape(label))
        else:
            href = os.path.relpath(target, os.path.dirname(here)).replace(os.sep, "/")
            items.append('<a href="%s">%s</a>' % (html.escape(href, quote=True),
                                                  html.escape(label)))
    if len(items) < 2:
        return ""
    return '<nav class="nav">%s</nav>' % "".join(items)


def page(md, src_name, md_path=None, planned=()):
    title = "Plan"
    for line in md.split("\n"):
        if line.startswith("# "):
            title = line[2:].strip(); break
    return ("""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<style>%s</style>
</head>
<body>
<div class="wrap">
%s<p class="src">Generated from %s — edit the markdown, not this file</p>
%s
</div>
</body>
</html>
""" % (html.escape(title), CSS, nav(md_path, planned) if md_path else "",
       html.escape(src_name), render(md)))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    check = "--check" in sys.argv[1:]
    if not args:
        sys.exit("usage: render_docs.py [--check] <file.md> [file.md ...]")

    planned = {os.path.abspath(p[:-3] + ".html")
               for p in args if p.endswith(".md") and os.path.isfile(p)}

    stale, wrote = [], 0
    for path in args:
        if not path.endswith(".md"):
            print("skip (not a .md file): %s" % path); continue
        if not os.path.isfile(path):
            print("skip (no such file): %s" % path); continue
        md = open(path, encoding="utf-8").read()
        out_path = path[:-3] + ".html"
        rendered = page(md, os.path.basename(path), path, planned)
        if check:
            current = (open(out_path, encoding="utf-8").read()
                       if os.path.exists(out_path) else None)
            if current != rendered:
                stale.append(out_path)
            continue
        open(out_path, "w", encoding="utf-8").write(rendered)
        print("wrote %s" % out_path); wrote += 1

    if check:
        if stale:
            print("%d stale HTML file(s) — run: python scripts/render_docs.py %s"
                  % (len(stale), " ".join(args)))
            for s in stale:
                print("  - %s" % s)
            return 1
        print("docs: up to date")
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
