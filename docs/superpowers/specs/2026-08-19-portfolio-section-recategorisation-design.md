# Portfolio section re-categorisation — design

Date: 2026-08-19
Status: approved

## Problem

The site presents five sections (hero, selected work, experience, writing, contact) but the
content inside them is not cleanly categorised:

1. **Education is filed under experience.** The BSc and the A-levels sit in the same
   `.timeline` component as the jobs, distinguished only by a dimmed dot. Resolved by
   removing the education content, not by promoting it to a section of its own.
2. **Two bodies of work are described twice.** The Research Intern role and project 01 are
   the same research; the Head of ML role and project 02 are the same racing stack. Each
   pair repeats the other's detail rather than dividing it.
3. **"Selected work" is not named what it is.** The section holds projects; the nav calls
   it "work".
4. **The writing section advertises posts that do not exist.** Three real-sounding titles
   sit under a note admitting they are placeholders.
5. **The hero's lead sentence does not parse:** "Computer Science student and the head of
   Machine Learning and Software Engineer."

## Scope

Restructure and re-categorise existing content. No new projects, roles or posts are
invented. The one piece of placeholder scaffolding on the page is the writing section,
whose three unwritten entries are labelled `planned` / `soon` (see section 4).

Education is removed from the site entirely — no education section, and the two education
entries are deleted from the experience timeline.

## Final section set and order

| # | Section | id | In nav |
| --- | --- | --- | --- |
| 1 | Landing / about (hero) | `top` | via brand link |
| 2 | Experience | `experience` | yes |
| 3 | Projects | `projects` | yes |
| 4 | Writing | `writing` | yes |
| 5 | Contact | `contact` | yes |

Nav order changes from `work · experience · writing · contact` to
`experience · projects · writing · contact`, matching page order.

## 1. Landing / about

Structure unchanged — the hero is the about section. One copy fix:

- `.hero__lead`: "Computer Science student and the head of Machine Learning and Software
  Engineer." → **"Computer Science student, Head of Machine Learning at Warwick Racing, and
  software engineer."**

Everything else in the hero (meta line, name, body paragraph) is untouched.

## 2. Experience — four entries, jobs only

The two education `.tl-item` blocks are deleted. The remaining four keep their order
(descending by start date). Section counter stays `2022 — now`, which is still correct.

### Split-by-lens rewrites

Experience answers *what was my role and responsibility*. Projects answers *what was built
and what came out*. Only the two entries with a project counterpart are rewritten.

**Research Intern, Artificial Intelligence and Machine Learning** — Apr 2026 — Jun 2026

> Awarded a competitive university bursary to run an independent research project on
> text-to-image person re-identification. Set the research direction and benchmarked the
> result against published academic baselines.

The "custom loss functions" detail is dropped here; project 01 already carries it.

**Head of Machine Learning, Warwick Racing** — Oct 2025 — present

> Own the perception and control stack against a strict latency budget. Work across the
> electrical and mechanical teams to get it onto the car.

(Corrected after review: the earlier wording said the role *set* the latency budget, which
overclaimed — the source text describes working to keep vision-to-command under 50 ms, a
constraint the role meets rather than authors.)

The tech inventory (segmentation CNNs, LiDAR clustering, RL and supervised steering, SQL,
Docker) moves out to project 02. The `50 ms` figure is deliberately not repeated here — the
hero and project 02 both already state it, and a third mention on one page is noise.

**Organiser — Logistics and Outreach (WHACK)** and **Founder and Lead Developer** are
unchanged. Neither has a project counterpart, so neither has anything to divide.

### Dot states

The site's convention is a bright `.tl-dot` for current entries and `.tl-dot--dim` for past
ones. Research Intern ended Jun 2026, so it moves to dim. Resulting states, in page order:

| Entry | Dates | Dot |
| --- | --- | --- |
| Research Intern | Apr 2026 — Jun 2026 | dim |
| Organiser, WHACK | Jan 2026 — present | bright |
| Head of ML, Warwick Racing | Oct 2025 — present | bright |
| Founder and Lead Developer | Jun 2022 — Sep 2024 | dim |

`.tl-item:last-child` tightening now applies to the Founder entry automatically.

## 3. Projects

Renamed in every visible place; internal class names are left alone.

- Heading text `selected work` → `projects`
- `id="work"` → `id="projects"`, and the nav href follows
- The `styles.css` section comment `--- selected work ---` → `--- projects ---`
- **Class names stay `.work-row`, `.work-row__num`, etc.** Renaming them is churn with no
  user-visible effect and is out of scope.

Four entries, numbering `01`–`04` unchanged, `.section__count` stays `04`.

Content changes: **project 02 gains a `SQL` tag.** "SQL over large datasets" currently
exists only in the Head of ML experience entry, and would otherwise be lost when that entry
is rewritten to the role lens. Project 02 tags become: PyTorch, OpenCV, ROS, Docker, SQL.

Project bodies for 01–04 are otherwise unchanged; they already sit on the outcome lens.

## 4. Writing

The three entries stay as a statement of intent, but stop pretending to be published:

- `.post-row__kind`: `notes` → `planned`
- `.post-row__when`: `placeholder` → `soon`
- The `<p class="section__note">` line is deleted
- The heading reverts from `section__head section__head--tight` to plain `section__head`,
  since the tight spacing existed only to sit above that note

## 5. Contact

Unchanged. Already last on the page.

## Dead CSS to remove

Both rules are used by the writing section only, and both become unused:

- `.section__head--tight` (`styles.css:213`)
- `.section__note` (`styles.css:225`)

`.section__head--wide` stays — the contact section still uses it.

## Files touched

| File | Change |
| --- | --- |
| `index.html` | Section order, nav, deletions, copy rewrites |
| `styles.css` | Remove two dead rules, rename one section comment |
| `README.md` | Four stale claims: the "A role" bullet's dot convention, the "A post" bullet calling the entries placeholders, the "A project" bullet's `work-row` walkthrough referencing the old section name, and the nav/section list implied by "Editing content" |

No new CSS components are needed. No JavaScript changes — `scripts/background.js` does not
reference any section.

## Out of scope

- Renaming `.work-row` CSS classes to `.project-row`
- Adding responsive breakpoints (the stylesheet is deliberately breakpoint-free and fluid)
- Writing real blog posts
- Any change to the background animation, favicon, or deploy workflow
