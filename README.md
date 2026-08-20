# josh beira — portfolio

A single-page portfolio site. No build step, no dependencies: plain HTML, one stylesheet,
one script. Built from the Claude Design canvas `Josh Beira - Portfolio v2.dc.html`.

## Run it locally

```bash
python3 -m http.server 8000
# → http://localhost:8000
```

It also works opened directly as a `file://` — every path is relative, which is the same
property that lets it live on a GitHub Pages project subpath.

## Layout

| Path | What it holds |
| --- | --- |
| `index.html` | All content. Projects and roles are written as markup, not loaded from JS. Sections run hero, work, experience, education, contact. |
| `styles.css` | Design tokens on `:root`, then one section of rules per page section. Block order does not track page order — the projects rules precede the experience timeline rules. |
| `scripts/background.js` | The animated graph-traversal canvas. Nothing else on the page depends on it. |
| `favicon.svg` | Two nodes and an edge, in the accent colour. |
| `.github/workflows/deploy.yml` | Builds nothing; uploads the repo root to GitHub Pages on push to `main`. |
| `.nojekyll` | Stops Pages running the files through Jekyll. |

## Editing content

Everything is in `index.html`, in the order it appears on the page.

- **A project** — copy an `<article class="work-row">` block in the `#work` section. The
  `work-row__num` is the hand-written index; update the count in the section header to
  match. One visible paragraph in `.work-row__summary`, everything longer inside the
  card's `<details class="disclose">`.
- **A role** — copy a `.tl-item` block in `#experience`. Solid `tl-dot` for current, add
  `tl-dot--dim` for ended. One visible paragraph in `.tl-item__summary`, the rest inside
  the disclosure.
- **An education entry** — copy a `.tl-item` block in `#education`. These carry no
  disclosure.

Long copy lives inside `<details class="disclose">`. The collapsed paragraph should stand
alone and read as a complete thought, not as a truncation.

## The background animation

`scripts/background.js` builds a graph across the viewport and animates a traversal over it,
then fades out and rebuilds. Two modes, switched by the footer buttons:

- **dijkstra** — a weighted lattice; the traversal is Dijkstra's algorithm, and once it
  settles the shortest path from the left edge to the right edge is drawn over the top.
- **bfs** — a jittered scatter graph explored breadth-first, no path pass.

Tuning knobs are the `DEFAULTS` object at the top of the file: `graphMode`,
`animationPresence` (0–100, how visible the graph is against the ground) and `accent`.

It respects `prefers-reduced-motion` by drawing the finished graph instantly rather than
animating, and pauses entirely while the tab is in the background.

## Deploying

Pushing to `main` deploys, with Pages set to **GitHub Actions** as its source
(Settings → Pages → Build and deployment → Source).

Live at <https://joshbeira.com>. The domain is set by the `CNAME` file at the repo root
and mirrored in the `canonical` and `og:url` tags in `index.html` — all three have to
agree, so change them together if the site ever moves again.
