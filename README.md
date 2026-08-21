# josh beira — portfolio

A portfolio site: a hand-written homepage plus one generated page per project under `/work/`.
No dependencies and no build step for the homepage; the project pages are rendered by a single
Python script. Built from the Claude Design canvas `Josh Beira - Portfolio v2.dc.html`.

## Run it locally

```bash
python3 -m http.server 8000
# → http://localhost:8000
```

Serve it — don't open it as a `file://`. The project pages and the icon set use root-absolute
paths (`/work/…`, `/img/…`), which is what lets the canonical URLs, the sitemap and the JSON-LD
`@id` values all agree on one address. That ties the site to a domain root, which is exactly what
`CNAME` gives it.

## Layout

| Path | What it holds |
| --- | --- |
| `index.html` | Homepage, hand-written. Projects and roles are markup, not loaded from JS. Sections run hero, experience, work, education, contact. Also holds the `Person` JSON-LD that anchors the site's SEO. |
| `work/` | **Generated.** Hub page plus one case-study page per project. Rebuilt by `tools/build_work_pages.py` — do not hand-edit. |
| `tools/build_work_pages.py` | Source of truth for the project pages and `sitemap.xml`. Edit `PROJECTS`, re-run. |
| `SEO.md` | What is set up, what still needs doing by hand, and what is realistic to rank for. |
| `llms.txt` | Plain-text site map for AI agents (llmstxt.org format). Hand-written, and it duplicates project descriptions — add a project, add it here too. |
| `styles.css` | Design tokens on `:root`, then one section of rules per page section. Block order does not track page order — the projects rules precede the experience timeline rules. |
| `scripts/background.js` | The animated graph-traversal canvas. Nothing else on the page depends on it. |
| `favicon.svg` | Two nodes and an edge, in the accent colour. Unused by the pages — the live icons are the generated PNGs below. |
| `favicon-32.png`, `icon-192.png`, `icon-512.png`, `apple-touch-icon.png` | Icon set, cropped from `profile.jpg`. |
| `img/` | Hero photo at display size, WebP + JPEG, 1× and 2×. `profile.jpg` is the uncropped master and is not served to the page. |
| `site.webmanifest` | Name, colours and icons for install prompts. |
| `.github/workflows/deploy.yml` | Builds nothing; uploads the repo root to GitHub Pages on push to `main`. |
| `googled2f802e0fa480847.html` | Google Search Console proof of ownership. **Do not delete or edit** — Google re-checks it, and removing it revokes the property. |
| `.nojekyll` | Stops Pages running the files through Jekyll. |

## Editing content

The homepage is in `index.html`, in the order it appears on the page. Project pages are generated —
see "Adding a project" below.

- **A project** — two places, and they have to agree. First add an entry to `PROJECTS` in
  `tools/build_work_pages.py` and run it; that writes the case-study page, the hub row and the
  sitemap. Then copy an `<article class="work-row">` block in the `#work` section of `index.html`,
  point its title at `/work/<slug>/`, and add the project to the `ItemList` in the homepage
  JSON-LD. The `work-row__num` is the hand-written index; update the count in the section header
  to match. One visible paragraph in `.work-row__summary`, everything longer inside the card's
  `<details class="disclose">`.
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

## Adding a project

```bash
# 1. edit PROJECTS in tools/build_work_pages.py
python3 tools/build_work_pages.py     # rewrites work/**/index.html and sitemap.xml
# 2. mirror it into index.html: a .work-row block + the ItemList entry in the JSON-LD
```

## Deploying

Pushing to `main` deploys, with Pages set to **GitHub Actions** as its source
(Settings → Pages → Build and deployment → Source).

Live at <https://joshbeira.com>. The domain is set by the `CNAME` file at the repo root and
mirrored in the `canonical` and `og:url` tags on every page, in the JSON-LD `@id` values, in
`sitemap.xml` and in `robots.txt`. If the site ever moves, change `CNAME`, `index.html`, and the
`SITE` constant in `tools/build_work_pages.py`, then re-run the generator.
