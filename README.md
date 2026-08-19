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
| `index.html` | All content. Projects, roles and posts are written as markup, not loaded from JS. |
| `styles.css` | Design tokens on `:root`, then one section of rules per page section. |
| `scripts/background.js` | The animated graph-traversal canvas. Nothing else on the page depends on it. |
| `favicon.svg` | Two nodes and an edge, in the accent colour. |
| `.github/workflows/deploy.yml` | Builds nothing; uploads the repo root to GitHub Pages on push to `main`. |
| `.nojekyll` | Stops Pages running the files through Jekyll. |

## Editing content

Everything is in `index.html`, in the order it appears on the page.

- **A project** — copy an `<article class="work-row">` block. The `work-row__num` is the
  hand-written index; update the `04` in the section header to match the count.
- **A role** — copy a `.tl-item` block. Use `<span class="tl-dot">` for current/highlighted
  entries and `<span class="tl-dot tl-dot--dim">` for past ones. The last item in the
  timeline automatically gets a tighter bottom padding.
- **A post** — copy a `<article class="post-row">` block. The three currently there are
  placeholders, as marked in the note above them.
- **Links on project and post rows** — these are `<article>` elements, not links, because
  the design had no destinations for them yet. To make one clickable, change the
  `<article class="work-row">` to `<a class="work-row" href="…">`; the hover treatment
  already works on both.

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
