# Portfolio Section Re-categorisation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Re-sort the portfolio's content into five correctly-scoped sections — landing, experience, projects, writing, contact — with education removed from the site entirely and the experience/projects overlap split onto separate lenses.

**Architecture:** This is a static site with no build step, no dependencies and no test framework. Every change is a text edit to `index.html`, `styles.css` or `README.md`. Verification is structural: a throwaway Python script asserts facts about the markup (section order, element counts, presence and absence of strings) and is run before and after each task to get a real red→green cycle. The script lives in the scratchpad and is **never committed** — the repo's dependency-free character is deliberate.

**Tech Stack:** Plain HTML5, hand-written CSS with custom properties, vanilla JS (untouched here). Python 3 for the local server and the verification script.

## Global Constraints

Copied from `docs/superpowers/specs/2026-08-19-portfolio-section-recategorisation-design.md`:

- **No new CSS components.** Removing education eliminated the only new component the design called for.
- **CSS class names do not change.** `.work-row`, `.work-row__num`, `.work-row__title`, `.work-row__body`, `.work-row__when` all keep their names. Only the visible heading, the `id`, the nav href and one CSS section comment change.
- **No new dependencies, no build step, no package manager, no test framework in the repo.**
- **No responsive breakpoints.** The stylesheet is deliberately breakpoint-free and fluid; do not add `@media` width queries.
- **Do not invent content.** No new projects, roles, posts or biographical facts. Every rewrite below recombines text that already exists on the page.
- **The verification script is never `git add`ed.** It lives only at `/tmp/claude-1000/-mnt-c-Users-Parham-OneDrive-Desktop-personal-website/833d5608-982a-449a-a39d-01dae24630f3/scratchpad/verify.py`.
- **Every edit is an exact-match string replacement asserted to hit exactly once.** Never use a loose regex or `replace_all` on these files — several target strings differ only by surrounding context.
- Repo root is `/mnt/c/Users/Parham/OneDrive/Desktop/personal_website`. Run every command from there.

---

### Task 1: Branch and verification harness

**Files:**
- Create: `/tmp/claude-1000/-mnt-c-Users-Parham-OneDrive-Desktop-personal-website/833d5608-982a-449a-a39d-01dae24630f3/scratchpad/verify.py` (scratchpad — not committed)
- Modify: none

**Interfaces:**
- Consumes: nothing.
- Produces: `verify.py`, runnable as `python3 <path>/verify.py` (all checks) or `python3 <path>/verify.py N` (only task N's checks). Exits `0` if every selected check passes, `1` otherwise. Every later task calls it.

- [ ] **Step 1: Create the feature branch**

The spec commit is already on `main`. All implementation work goes on a branch.

```bash
cd /mnt/c/Users/Parham/OneDrive/Desktop/personal_website
git checkout -b recategorise-sections
git status -sb
```

Expected: `## recategorise-sections`, clean tree.

- [ ] **Step 2: Write the verification script**

```bash
cat > /tmp/claude-1000/-mnt-c-Users-Parham-OneDrive-Desktop-personal-website/833d5608-982a-449a-a39d-01dae24630f3/scratchpad/verify.py <<'PYEOF'
#!/usr/bin/env python3
"""Structural checks for the portfolio re-categorisation.

Throwaway harness - lives in the scratchpad, never committed. The repo has no
test framework by design, so this asserts facts about the markup instead.

Usage:  python3 verify.py        # every check
        python3 verify.py 3      # only task 3's checks
"""
import re
import sys
import pathlib

ROOT = pathlib.Path("/mnt/c/Users/Parham/OneDrive/Desktop/personal_website")
html = (ROOT / "index.html").read_text(encoding="utf-8")
css = (ROOT / "styles.css").read_text(encoding="utf-8")
readme = (ROOT / "README.md").read_text(encoding="utf-8")

CHECKS = []


def check(task, name):
    def deco(fn):
        CHECKS.append((task, name, fn))
        return fn
    return deco


def projects_id():
    """The projects section is id=work before task 4 and id=projects after."""
    return "projects" if 'id="projects"' in html else "work"


def section_ids():
    return re.findall(r'<section[^>]*\bid="([\w-]+)"', html)


def nav_hrefs():
    nav = re.search(r'<nav class="nav".*?</nav>', html, re.S).group(0)
    return re.findall(r'<a href="#([\w-]+)">', nav)


# --- task 2: section and nav order ------------------------------------------

@check(2, "sections run experience -> projects -> writing -> contact")
def _():
    want = ["experience", projects_id(), "writing", "contact"]
    got = section_ids()
    assert got == want, f"got {got}, want {want}"


@check(2, "nav order matches page order")
def _():
    want = ["experience", projects_id(), "writing", "contact"]
    got = nav_hrefs()
    assert got == want, f"got {got}, want {want}"


@check(2, "section tags stay balanced")
def _():
    o, c = html.count("<section"), html.count("</section>")
    assert o == c, f"{o} open vs {c} close"


# --- task 3: experience is jobs only, split onto the role lens --------------

@check(3, "no education content anywhere in the page")
def _():
    for term in ("BSc", "A-levels", "Cadbury", "Sep 2025 — Jul 2028",
                 "Sep 2023 — Jun 2025", "EPQ"):
        assert term not in html, f"{term!r} still present"


@check(3, "experience timeline has exactly 4 entries")
def _():
    n = html.count('class="tl-item"')
    assert n == 4, f"{n} tl-item blocks, want 4"


@check(3, "Research Intern dot is dimmed (role ended Jun 2026)")
def _():
    block = re.search(r'<div class="tl-item">\s*<div class="tl-when">Apr 2026 [^<]*</div>.*?</div>\s*</div>',
                      html, re.S)
    assert block, "Research Intern tl-item not found"
    assert "tl-dot tl-dot--dim" in block.group(0), "dot is still bright"


@check(3, "Research Intern note is on the role lens")
def _():
    assert "Set the research direction and benchmarked the result against published academic baselines." in html
    assert "Formulated custom loss functions" not in html, "old note text survives"


@check(3, "Head of ML note is on the role lens")
def _():
    assert "Own the perception and control stack against a strict latency budget." in html
    assert "image-segmentation CNNs with LiDAR clustering" not in html, "tech inventory survives in experience"


@check(3, "the 50 ms figure is not repeated a third time")
def _():
    n = len(re.findall(r"50\s?m", html))
    assert n == 2, f"{n} mentions of 50 ms, want 2 (hero + project 02)"


# --- task 4: projects rename + SQL tag --------------------------------------

@check(4, "section is named and anchored 'projects'")
def _():
    assert 'id="projects"' in html
    assert "<h2>projects</h2>" in html
    assert 'href="#projects"' in html


@check(4, "no trace of the old 'work' naming")
def _():
    assert 'id="work"' not in html
    assert 'href="#work"' not in html
    assert "selected work" not in html
    assert "selected work" not in css


@check(4, "CSS class names were NOT renamed")
def _():
    for cls in ("work-row", "work-row__num", "work-row__title",
                "work-row__body", "work-row__when"):
        assert cls in html, f".{cls} missing from markup"
        assert cls in css, f".{cls} missing from stylesheet"


@check(4, "project 02 carries the SQL tag moved out of experience")
def _():
    block = re.search(r'<span class="work-row__num"[^>]*>02</span>.*?</article>', html, re.S)
    assert block, "project 02 not found"
    assert '<span class="tag">SQL</span>' in block.group(0), "SQL tag missing"


@check(4, "stylesheet section comment renamed")
def _():
    assert "/* --- projects " in css


# --- task 5: writing marked as planned, dead CSS gone -----------------------

@check(5, "all three posts are labelled planned / soon")
def _():
    k = html.count('<span class="post-row__kind">planned</span>')
    w = html.count('<span class="post-row__when">soon</span>')
    assert k == 3, f"{k} 'planned' labels, want 3"
    assert w == 3, f"{w} 'soon' labels, want 3"
    assert "notes</span>" not in html
    assert "placeholder</span>" not in html


@check(5, "the placeholder note is gone from markup and stylesheet")
def _():
    assert "section__note" not in html
    assert "section__note" not in css


@check(5, "the --tight head modifier is gone from markup and stylesheet")
def _():
    assert "section__head--tight" not in html
    assert "section__head--tight" not in css


@check(5, "--wide survives (contact still uses it)")
def _():
    assert "section__head--wide" in html
    assert "section__head--wide" in css


# --- task 6: hero lead sentence --------------------------------------------

@check(6, "hero lead parses as a sentence")
def _():
    assert ("Computer Science student, Head of Machine Learning at Warwick Racing, "
            "and software engineer.") in html
    assert "and the head of Machine Learning and Software Engineer" not in html


# --- task 7: README matches reality ----------------------------------------

@check(7, "README does not describe the deleted note or placeholders")
def _():
    assert "as marked in the note above them" not in readme
    assert "placeholder" not in readme.lower()


@check(7, "README does not use the old section name")
def _():
    assert "selected work" not in readme.lower()


@check(7, "README documents the education removal is not needed anywhere")
def _():
    for term in ("BSc", "A-levels", "Cadbury"):
        assert term not in readme, f"{term!r} in README"


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    selected = [c for c in CHECKS if only is None or str(c[0]) == only]
    if not selected:
        print(f"no checks for task {only}")
        return 1
    failed = 0
    for task, name, fn in selected:
        try:
            fn()
            print(f"  PASS  [t{task}] {name}")
        except AssertionError as e:
            failed += 1
            print(f"  FAIL  [t{task}] {name}: {e}")
    total = len(selected)
    print(f"\n{total - failed}/{total} passing")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
PYEOF
echo written
```

- [ ] **Step 3: Run it to confirm everything is red**

```bash
python3 /tmp/claude-1000/-mnt-c-Users-Parham-OneDrive-Desktop-personal-website/833d5608-982a-449a-a39d-01dae24630f3/scratchpad/verify.py; echo "exit=$?"
```

Expected: `exit=1`, with FAIL lines for tasks 2–7. A handful of checks may already pass incidentally (for example "section tags stay balanced" and "CSS class names were NOT renamed" are true before any edit) — that is correct, they are regression guards, not new behaviour.

- [ ] **Step 4: No commit**

Nothing to commit — the harness is scratchpad-only and the repo is untouched. Confirm:

```bash
git status --porcelain
```

Expected: empty output.

---

### Task 2: Reorder sections and nav to CV order

**Files:**
- Modify: `index.html` (nav lines 42–45; move the `#work` section block, currently lines 65–131, to sit after the `#experience` block)

**Interfaces:**
- Consumes: `verify.py` from Task 1.
- Produces: page order `hero → experience → work → writing → contact`. The section still carries `id="work"`; Task 4 renames it. Later tasks locate sections by `id`, not by line number, so this move is safe to do first.

Doing the move *before* any copy edits keeps this diff a pure block relocation, which is far easier to review than a move tangled with rewrites.

- [ ] **Step 1: Confirm task 2's checks currently fail**

```bash
cd /mnt/c/Users/Parham/OneDrive/Desktop/personal_website
python3 /tmp/claude-1000/-mnt-c-Users-Parham-OneDrive-Desktop-personal-website/833d5608-982a-449a-a39d-01dae24630f3/scratchpad/verify.py 2; echo "exit=$?"
```

Expected: `exit=1`. The order checks report `got ['work', 'experience', 'writing', 'contact']`.

- [ ] **Step 2: Swap the two section blocks and reorder the nav**

```bash
cd /mnt/c/Users/Parham/OneDrive/Desktop/personal_website
python3 - <<'PYEOF'
import pathlib

p = pathlib.Path("index.html")
s = p.read_text(encoding="utf-8")

# --- swap the section blocks (work currently precedes experience) ---
work_start = s.index('    <section id="work" class="section">')
exp_start = s.index('    <section id="experience" class="section">')
writing_start = s.index('    <section id="writing" class="section">')
assert work_start < exp_start < writing_start, "unexpected starting order"

work_block = s[work_start:exp_start]
exp_block = s[exp_start:writing_start]
s = s[:work_start] + exp_block + work_block + s[writing_start:]

# --- reorder the nav to match ---
old_nav = '''      <a href="#work">work</a>
      <a href="#experience">experience</a>'''
new_nav = '''      <a href="#experience">experience</a>
      <a href="#work">work</a>'''
assert s.count(old_nav) == 1, f"nav match count {s.count(old_nav)}"
s = s.replace(old_nav, new_nav)

p.write_text(s, encoding="utf-8")
print("reordered")
PYEOF
```

- [ ] **Step 3: Verify task 2 is green**

```bash
python3 /tmp/claude-1000/-mnt-c-Users-Parham-OneDrive-Desktop-personal-website/833d5608-982a-449a-a39d-01dae24630f3/scratchpad/verify.py 2; echo "exit=$?"
```

Expected: `exit=0`, `3/3 passing`.

- [ ] **Step 4: Sanity-check the diff is a pure move**

```bash
git diff --stat index.html
```

Expected: a single file with roughly equal insertions and deletions and no net line-count change beyond the nav swap.

- [ ] **Step 5: Commit**

```bash
git add index.html
git commit -m "Reorder page and nav into CV order

Experience now precedes the projects section, matching the nav."
```

---

### Task 3: Strip education from experience and split onto the role lens

**Files:**
- Modify: `index.html` (the `#experience` section — delete two `.tl-item` blocks, rewrite two `.tl-note` paragraphs, dim one `.tl-dot`)

**Interfaces:**
- Consumes: reordered markup from Task 2.
- Produces: a four-entry timeline containing only jobs. The technical detail removed from the Head of ML entry is picked up by Task 4, which adds the `SQL` tag to project 02.

- [ ] **Step 1: Confirm task 3's checks currently fail**

```bash
cd /mnt/c/Users/Parham/OneDrive/Desktop/personal_website
python3 /tmp/claude-1000/-mnt-c-Users-Parham-OneDrive-Desktop-personal-website/833d5608-982a-449a-a39d-01dae24630f3/scratchpad/verify.py 3; echo "exit=$?"
```

Expected: `exit=1`, six FAIL lines.

- [ ] **Step 2: Apply all four experience edits**

```bash
cd /mnt/c/Users/Parham/OneDrive/Desktop/personal_website
python3 - <<'PYEOF'
import pathlib

p = pathlib.Path("index.html")
s = p.read_text(encoding="utf-8")

edits = []

# 1 + 2. Research Intern: dim the dot and move onto the role lens.
# Replaced as a whole block because the bare <span class="tl-dot"> line is not unique.
edits.append((
'''        <div class="tl-item">
          <div class="tl-when">Apr 2026 — Jun 2026</div>
          <div class="tl-body">
            <span class="tl-dot" aria-hidden="true"></span>
            <h3 class="tl-role">Research Intern, Artificial Intelligence and Machine Learning</h3>
            <p class="tl-org">Dept. of Computer Science, University of Warwick</p>
            <p class="tl-note">Awarded a competitive university bursary for independent research into a more efficient approach to text-to-image person re-identification. Formulated custom loss functions and benchmarked against academic baselines.</p>
          </div>
        </div>''',
'''        <div class="tl-item">
          <div class="tl-when">Apr 2026 — Jun 2026</div>
          <div class="tl-body">
            <span class="tl-dot tl-dot--dim" aria-hidden="true"></span>
            <h3 class="tl-role">Research Intern, Artificial Intelligence and Machine Learning</h3>
            <p class="tl-org">Dept. of Computer Science, University of Warwick</p>
            <p class="tl-note">Awarded a competitive university bursary to run an independent research project on text-to-image person re-identification. Set the research direction and benchmarked the result against published academic baselines.</p>
          </div>
        </div>'''))

# 3. Head of ML: keep ownership and cross-team scope, drop the tech inventory
#    and the repeated latency figure (the hero and project 02 both carry it).
edits.append((
'''            <p class="tl-note">Own the perception and control stack: image-segmentation CNNs with LiDAR clustering, RL and supervised steering models, SQL over large datasets, Docker delivery. Work across the electrical and mechanical teams to keep vision-to-command under 50 ms.</p>''',
'''            <p class="tl-note">Own the perception and control stack against a strict latency budget. Work across the electrical and mechanical teams to get it onto the car.</p>'''))

# 4. Delete both education entries outright.
edits.append((
'''
        <div class="tl-item">
          <div class="tl-when">Sep 2025 — Jul 2028</div>
          <div class="tl-body">
            <span class="tl-dot tl-dot--dim" aria-hidden="true"></span>
            <h3 class="tl-role">BSc (Hons) Computer Science</h3>
            <p class="tl-org">University of Warwick</p>
            <p class="tl-note">Coventry, UK.</p>
          </div>
        </div>

        <div class="tl-item">
          <div class="tl-when">Sep 2023 — Jun 2025</div>
          <div class="tl-body">
            <span class="tl-dot tl-dot--dim" aria-hidden="true"></span>
            <h3 class="tl-role">A-levels — A*A*A*A*A*</h3>
            <p class="tl-org">Cadbury Sixth Form, Birmingham</p>
            <p class="tl-note">Mathematics, Further Mathematics, Computer Science, Physics, EPQ.</p>
          </div>
        </div>
''', ''))

for i, (old, new) in enumerate(edits, 1):
    n = s.count(old)
    assert n == 1, f"edit {i}: matched {n} times, expected exactly 1"
    s = s.replace(old, new)

p.write_text(s, encoding="utf-8")
print(f"{len(edits)} edits applied")
PYEOF
```

- [ ] **Step 3: Verify task 3 is green**

```bash
python3 /tmp/claude-1000/-mnt-c-Users-Parham-OneDrive-Desktop-personal-website/833d5608-982a-449a-a39d-01dae24630f3/scratchpad/verify.py 3; echo "exit=$?"
```

Expected: `exit=0`, `6/6 passing`.

- [ ] **Step 4: Confirm the timeline still closes cleanly**

```bash
sed -n '/<div class="timeline">/,/<\/section>/p' index.html | tail -20
```

Expected: the Founder entry, then a blank line, then `      </div>` and `    </section>` — no orphaned blank lines or stray `</div>`.

- [ ] **Step 5: Commit**

```bash
git add index.html
git commit -m "Remove education and split experience onto the role lens

Deletes the BSc and A-level timeline entries. Rewrites the Research Intern
and Head of ML notes to describe responsibility rather than repeating the
technical detail that projects already carries, and dims the Research
Intern dot now that the role has ended."
```

---

### Task 4: Rename "selected work" to projects and add the SQL tag

**Files:**
- Modify: `index.html` (section `id`, `<h2>`, nav href, project 02 tag list)
- Modify: `styles.css` (one section comment)

**Interfaces:**
- Consumes: the four-entry experience section from Task 3.
- Produces: `id="projects"` and `href="#projects"`. No later task depends on the old `#work` anchor; a repo-wide search confirmed it is referenced nowhere outside `index.html` — `sitemap.xml` lists only the root URL and `404.html` links only to `/`.

- [ ] **Step 1: Confirm task 4's checks currently fail**

```bash
cd /mnt/c/Users/Parham/OneDrive/Desktop/personal_website
python3 /tmp/claude-1000/-mnt-c-Users-Parham-OneDrive-Desktop-personal-website/833d5608-982a-449a-a39d-01dae24630f3/scratchpad/verify.py 4; echo "exit=$?"
```

Expected: `exit=1`. The "CSS class names were NOT renamed" check should already PASS — it is a guard against over-eager renaming in this very task.

- [ ] **Step 2: Rename the visible identifiers and add the tag**

```bash
cd /mnt/c/Users/Parham/OneDrive/Desktop/personal_website
python3 - <<'PYEOF'
import pathlib

html_p, css_p = pathlib.Path("index.html"), pathlib.Path("styles.css")
html, css = html_p.read_text(encoding="utf-8"), css_p.read_text(encoding="utf-8")

html_edits = [
    ('<section id="work" class="section">', '<section id="projects" class="section">'),
    ('<h2>selected work</h2>', '<h2>projects</h2>'),
    ('<a href="#work">work</a>', '<a href="#projects">projects</a>'),
    # SQL moves here from the Head of ML experience note rewritten in task 3.
    # This four-tag run is unique to project 02.
    ('''          <span class="tag">PyTorch</span>
          <span class="tag">OpenCV</span>
          <span class="tag">ROS</span>
          <span class="tag">Docker</span>''',
     '''          <span class="tag">PyTorch</span>
          <span class="tag">OpenCV</span>
          <span class="tag">ROS</span>
          <span class="tag">Docker</span>
          <span class="tag">SQL</span>'''),
]

for i, (old, new) in enumerate(html_edits, 1):
    n = html.count(old)
    assert n == 1, f"html edit {i}: matched {n} times, expected exactly 1"
    html = html.replace(old, new)

# Rebuild the comment ruler to the identical total width as the original.
old_c = '/* --- selected work -------------------------------------------------------- */'
assert css.count(old_c) == 1, f"css comment matched {css.count(old_c)} times"
head = '/* --- projects '
new_c = head + '-' * (len(old_c) - len(head) - 3) + ' */'
assert len(new_c) == len(old_c), "ruler width drifted"
css = css.replace(old_c, new_c)

html_p.write_text(html, encoding="utf-8")
css_p.write_text(css, encoding="utf-8")
print("renamed; SQL tag added")
PYEOF
```

- [ ] **Step 3: Verify task 4 is green**

```bash
python3 /tmp/claude-1000/-mnt-c-Users-Parham-OneDrive-Desktop-personal-website/833d5608-982a-449a-a39d-01dae24630f3/scratchpad/verify.py 4; echo "exit=$?"
```

Expected: `exit=0`, `5/5 passing`.

- [ ] **Step 4: Commit**

```bash
git add index.html styles.css
git commit -m "Rename selected work to projects

Heading, anchor, nav href and the stylesheet section comment. CSS class
names keep the work-row prefix. Project 02 picks up the SQL tag that the
Head of ML experience entry used to carry."
```

---

### Task 5: Mark the writing entries as planned and drop the dead CSS

**Files:**
- Modify: `index.html` (writing section head class, the note paragraph, six span contents)
- Modify: `styles.css` (delete `.section__head--tight` and the `.section__note` rule)

**Interfaces:**
- Consumes: markup from Task 4.
- Produces: nothing later tasks depend on, except that Task 7's README edits describe this section's new state.

- [ ] **Step 1: Confirm task 5's checks currently fail**

```bash
cd /mnt/c/Users/Parham/OneDrive/Desktop/personal_website
python3 /tmp/claude-1000/-mnt-c-Users-Parham-OneDrive-Desktop-personal-website/833d5608-982a-449a-a39d-01dae24630f3/scratchpad/verify.py 5; echo "exit=$?"
```

Expected: `exit=1`. The "--wide survives" check should already PASS — it guards against deleting the wrong modifier here.

- [ ] **Step 2: Relabel the posts and remove the now-unused rules**

```bash
cd /mnt/c/Users/Parham/OneDrive/Desktop/personal_website
python3 - <<'PYEOF'
import pathlib

html_p, css_p = pathlib.Path("index.html"), pathlib.Path("styles.css")
html, css = html_p.read_text(encoding="utf-8"), css_p.read_text(encoding="utf-8")

# The tight head only existed to sit above the note; both go together.
one_offs = [
    ('<div class="section__head section__head--tight">', '<div class="section__head">'),
    ('''      <p class="section__note">placeholder entries — send real posts and I'll swap them in.</p>\n''', ''),
]
for i, (old, new) in enumerate(one_offs, 1):
    n = html.count(old)
    assert n == 1, f"html edit {i}: matched {n} times, expected exactly 1"
    html = html.replace(old, new)

# Three of each, all identical - replace every occurrence.
for old, new, want in [
    ('<span class="post-row__kind">notes</span>',
     '<span class="post-row__kind">planned</span>', 3),
    ('<span class="post-row__when">placeholder</span>',
     '<span class="post-row__when">soon</span>', 3),
]:
    n = html.count(old)
    assert n == want, f"matched {n} times, expected {want}"
    html = html.replace(old, new)

css_removals = [
    '.section__head--tight { margin-bottom: 12px; }\n',
    # Trailing newline only, NOT the blank line after it - that blank line
    # separates the section-scaffolding group from .list-end and must survive.
    '''.section__note {
  margin-bottom: 24px;
  font-family: var(--mono);
  font-size: 11px;
  color: var(--faint);
}
''',
]
for i, old in enumerate(css_removals, 1):
    n = css.count(old)
    assert n == 1, f"css removal {i}: matched {n} times, expected exactly 1"
    css = css.replace(old, '')

# --wide was padded with two spaces to align with --tight; with --tight gone
# that padding is orphaned.
old_wide = '.section__head--wide  { margin-bottom: 36px; }'
assert css.count(old_wide) == 1, "unexpected --wide formatting"
css = css.replace(old_wide, '.section__head--wide { margin-bottom: 36px; }')

assert '.section__head--wide' in css, "removed the wrong modifier"

html_p.write_text(html, encoding="utf-8")
css_p.write_text(css, encoding="utf-8")
print("writing section relabelled; 2 dead rules removed")
PYEOF
```

- [ ] **Step 3: Verify task 5 is green**

```bash
python3 /tmp/claude-1000/-mnt-c-Users-Parham-OneDrive-Desktop-personal-website/833d5608-982a-449a-a39d-01dae24630f3/scratchpad/verify.py 5; echo "exit=$?"
```

Expected: `exit=0`, `4/4 passing`.

- [ ] **Step 4: Confirm no other rule referenced the deleted ones**

```bash
grep -n "section__note\|section__head--tight" index.html styles.css 404.html; echo "grep exit=$?"
sed -n '/section__head--wide/,/list-end/p' styles.css
```

Expected: no grep output and `grep exit=1` (no matches) — note `404.html` shares the
stylesheet, so it is checked too. The `sed` output should show `.section__head--wide` with
single-space padding, and a blank line still separating `.section__count` from `.list-end`.

- [ ] **Step 5: Commit**

```bash
git add index.html styles.css
git commit -m "Mark unwritten posts as planned rather than placeholder

The three entries now read planned / soon and the apologetic note above
them is gone, which also retires .section__note and .section__head--tight."
```

---

### Task 6: Fix the hero lead sentence

**Files:**
- Modify: `index.html` (the `.hero__lead` paragraph)

**Interfaces:**
- Consumes: markup from Task 5.
- Produces: nothing later tasks depend on.

The current sentence fuses two roles with a stray conjunction and does not parse: *"Computer Science student and the head of Machine Learning and Software Engineer."*

- [ ] **Step 1: Confirm task 6's check currently fails**

```bash
cd /mnt/c/Users/Parham/OneDrive/Desktop/personal_website
python3 /tmp/claude-1000/-mnt-c-Users-Parham-OneDrive-Desktop-personal-website/833d5608-982a-449a-a39d-01dae24630f3/scratchpad/verify.py 6; echo "exit=$?"
```

Expected: `exit=1`, one FAIL.

- [ ] **Step 2: Rewrite the sentence**

```bash
cd /mnt/c/Users/Parham/OneDrive/Desktop/personal_website
python3 - <<'PYEOF'
import pathlib

p = pathlib.Path("index.html")
s = p.read_text(encoding="utf-8")

old = '<p class="hero__lead">Computer Science student and the head of Machine Learning and Software Engineer.</p>'
new = '<p class="hero__lead">Computer Science student, Head of Machine Learning at Warwick Racing, and software engineer.</p>'
assert s.count(old) == 1, f"matched {s.count(old)} times"
p.write_text(s.replace(old, new), encoding="utf-8")
print("hero lead rewritten")
PYEOF
```

- [ ] **Step 3: Verify task 6 is green**

```bash
python3 /tmp/claude-1000/-mnt-c-Users-Parham-OneDrive-Desktop-personal-website/833d5608-982a-449a-a39d-01dae24630f3/scratchpad/verify.py 6; echo "exit=$?"
```

Expected: `exit=0`, `1/1 passing`.

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "Fix the hero lead sentence

Two roles were fused with a stray conjunction into something that did not
parse."
```

---

### Task 7: Update the README and verify the whole page

**Files:**
- Modify: `README.md` (the "Layout" table row for `index.html`, and three bullets under "Editing content")

**Interfaces:**
- Consumes: the finished markup from Tasks 2–6.
- Produces: the final state. This task ends with the full check suite green and a visual confirmation in a real browser.

The README currently documents the pre-change structure: it names the section "selected work" via the `work-row` walkthrough, tells the reader to use a bright dot for "current/highlighted" entries, and describes the writing entries as placeholders "as marked in the note above them" — a note that no longer exists.

- [ ] **Step 1: Confirm task 7's checks currently fail**

```bash
cd /mnt/c/Users/Parham/OneDrive/Desktop/personal_website
python3 /tmp/claude-1000/-mnt-c-Users-Parham-OneDrive-Desktop-personal-website/833d5608-982a-449a-a39d-01dae24630f3/scratchpad/verify.py 7; echo "exit=$?"
```

Expected: `exit=1`, at least two FAILs.

- [ ] **Step 2: Bring the README in line with the page**

```bash
cd /mnt/c/Users/Parham/OneDrive/Desktop/personal_website
python3 - <<'PYEOF'
import pathlib

p = pathlib.Path("README.md")
s = p.read_text(encoding="utf-8")

edits = [
(
'''| `index.html` | All content. Projects, roles and posts are written as markup, not loaded from JS. |''',
'''| `index.html` | All content. Projects, roles and posts are written as markup, not loaded from JS. Sections run hero, experience, projects, writing, contact. |'''
),
(
'''- **A project** — copy an `<article class="work-row">` block. The `work-row__num` is the
  hand-written index; update the `04` in the section header to match the count.''',
'''- **A project** — copy an `<article class="work-row">` block in the `#projects` section.
  The `work-row__num` is the hand-written index; update the `04` in the section header to
  match the count. The class prefix is still `work-row` even though the section is now
  called projects — the markup was left alone when the heading was renamed.'''
),
(
'''- **A role** — copy a `.tl-item` block. Use `<span class="tl-dot">` for current/highlighted
  entries and `<span class="tl-dot tl-dot--dim">` for past ones. The last item in the
  timeline automatically gets a tighter bottom padding.''',
'''- **A role** — copy a `.tl-item` block in the `#experience` section. Use
  `<span class="tl-dot">` for roles you currently hold and
  `<span class="tl-dot tl-dot--dim">` for ones that have ended. The last item in the
  timeline automatically gets a tighter bottom padding. Experience is jobs only; the site
  carries no education section.'''
),
(
'''- **A post** — copy a `<article class="post-row">` block. The three currently there are
  placeholders, as marked in the note above them.''',
'''- **A post** — copy a `<article class="post-row">` block. The three currently there are
  unwritten, and say so: their `post-row__kind` reads `planned` and their `post-row__when`
  reads `soon`. When one goes live, change those two spans to `notes` and the date.'''
),
]

for i, (old, new) in enumerate(edits, 1):
    n = s.count(old)
    assert n == 1, f"readme edit {i}: matched {n} times, expected exactly 1"
    s = s.replace(old, new)

p.write_text(s, encoding="utf-8")
print(f"{len(edits)} README edits applied")
PYEOF
```

- [ ] **Step 3: Run the entire suite**

```bash
python3 /tmp/claude-1000/-mnt-c-Users-Parham-OneDrive-Desktop-personal-website/833d5608-982a-449a-a39d-01dae24630f3/scratchpad/verify.py; echo "exit=$?"
```

Expected: `exit=0` and every line PASS — 22/22 passing.

- [ ] **Step 4: Look at the actual page**

Structural checks cannot see layout. Serve the site and confirm it renders.

```bash
cd /mnt/c/Users/Parham/OneDrive/Desktop/personal_website
python3 -m http.server 8000 >/dev/null 2>&1 &
sleep 1
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000/
```

Expected: `200`. Then open `http://localhost:8000/` and confirm by eye:

1. Sections run hero → experience → projects → writing → contact.
2. The experience timeline has four entries and no qualifications.
3. Only the two `present` roles (WHACK, Warwick Racing) have a bright dot.
4. The projects heading reads `projects`, still counts `04`, and project 02 shows five tags ending in `SQL`.
5. The writing rows read `planned` / `soon` with no note above them, and the gap between the heading and the first row matches the other sections.
6. Clicking each nav item scrolls to the right section.

Stop the server when done:

```bash
kill %1
```

- [ ] **Step 5: Commit**

```bash
git add README.md
git commit -m "Update README for the re-categorised sections

Documents the new section order, the projects rename, the jobs-only
experience timeline and the planned/soon post labels."
```

- [ ] **Step 6: Confirm the scratchpad harness was never committed**

```bash
git status --porcelain
git log --oneline main..HEAD
grep -rn "verify.py" . --exclude-dir=.git || echo "verify.py not referenced in the repo"
```

Expected: clean tree, six commits on the branch, and no reference to `verify.py` anywhere in tracked files (this plan document mentions the path, which is fine — it lives under `docs/superpowers/plans/` and is committed on `main`).

---

## Self-Review

**Spec coverage**

| Spec requirement | Task |
| --- | --- |
| Section order landing → experience → projects → writing → contact | 2 |
| Nav reordered, 4 items | 2, 4 |
| Hero lead sentence fixed | 6 |
| Education deleted entirely (both entries, no section) | 3 |
| Research Intern rewritten to role lens | 3 |
| Head of ML rewritten to role lens | 3 |
| WHACK and Founder untouched | 3 (asserted by the 4-entry count) |
| Research Intern dot dimmed | 3 |
| Experience counter stays `2022 — now` | untouched by any task — no edit targets it |
| Heading, id, nav href, CSS comment renamed to projects | 4 |
| `.work-row` class names preserved | 4 (explicit guard check) |
| Project 02 gains SQL tag | 4 |
| Projects counter stays `04` | untouched by any task |
| Writing: planned / soon, note deleted, head modifier dropped | 5 |
| `.section__head--tight` and `.section__note` removed | 5 |
| `.section__head--wide` preserved | 5 (explicit guard check) |
| Contact unchanged | no task touches it |
| README updated | 7 |
| No new CSS components | no task adds CSS |

No gaps.

**Placeholder scan:** No TBD/TODO, no "add error handling", no "similar to Task N". Every code step contains the literal text to run.

**Type consistency:** The only cross-task contract is `verify.py`'s CLI — `python3 verify.py [N]`, exit 0/1 — defined in Task 1 and called identically in Tasks 2–7. `projects_id()` deliberately tolerates both `work` and `projects` so Task 2's checks keep passing after Task 4 renames the anchor.
