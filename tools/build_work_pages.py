#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Builds /work/ (hub + one page per project) and sitemap.xml.

The pages under work/ are GENERATED — edit PROJECTS below and re-run, do not
hand-edit the HTML. index.html is NOT generated; it is written by hand, and the
ItemList in its JSON-LD has to be kept in step with PROJECTS by hand too.

    python3 tools/build_work_pages.py
"""
# Content is expanded from what already exists in index.html. No metric, result or
# claim here that is not already stated on the site — the TODO notes in index.html
# record which figures were placeholders, and none of those are reintroduced.

SITE = "https://joshbeira.com"

PROJECTS = [
{
 "slug": "pdtbench",
 "num": "01",
 "h1": "pdtbench — an agentic trading benchmark with a control group",
 "nav_title": "pdtbench",
 "title": "pdtbench — an agentic trading benchmark | Josh Beira",
 "desc": "An LLM trading benchmark that separates skill from memorising the chart — every real market window is paired with a synthetic twin. 1st at the PDT hackathon.",
 "kicker": "2026 · PDT Partners hackathon — 1st place",
 "date": "2026-07-01",
 "lead": "A language model makes money on a historical market window. Is that skill, or does it remember the chart? Every real window gets a synthetic twin, so you can tell the difference.",
 "tags": ["Python", "MCP", "Streamlit", "Parquet", "pytest"],
 "langs": ["Python"],
 "repo": "https://github.com/joshbeira/Agentic-Trading-Benchmark-PDT-Hackathon-",
 "demo": None,
 "keywords": ["agentic benchmark", "LLM evaluation", "quantitative trading", "backtesting",
              "data contamination", "memorisation", "Model Context Protocol", "Sharpe ratio"],
 "sections": [
   ("the question this answers",
    ["<p>Give a language model a historical market window and it will often turn a profit. That number "
     "on its own is close to meaningless: the model may have read the chart during pretraining. Standard "
     "backtests cannot separate a model that trades well from a model that remembers what happened next.</p>",
     "<p>pdtbench is built around a control group, the way a trial is. It was built at the PDT Partners "
     "hackathon, where it took first place.</p>"]),
   ("the synthetic twin",
    ["<p>Every real window is paired with a synthetic twin — matched on total return (±3pp), volatility "
     "(±15%) and regime, so the trade to make is identical and only the identity differs. The twin is the "
     "same problem stripped of anything the model could have memorised.</p>",
     "<p>Beating the real window by more than its twin is the edge. That gap, not the raw return, is the "
     "score that means something.</p>"]),
   ("memorisation as a measurable slope",
    ["<p>Regressing that gap against how often the model can name the window turns “is this memorisation?” "
     "into a slope you can measure, rather than a suspicion you argue about.</p>"]),
   ("no look-ahead, by construction",
    ["<p>The engine fills at the next unseen open, and a read-audit test makes look-ahead impossible by "
     "construction rather than by convention.</p>",
     "<p>Baselines and the agent enter through the same in-process MCP server, so fee parity holds by "
     "construction rather than by assertion. Neither side can be quietly advantaged by a different code path.</p>"]),
   ("a scoring rule that cannot be gamed by sitting out",
    ["<p>Sharpe is floored at 0.25 × buy-and-hold daily volatility, because plain Sharpe on a mostly-cash "
     "account rewards deploying 1% of capital for two lucky days. An agent that never trades scores exactly zero.</p>"]),
   ("state of the work",
    ["<p>218 tests, none touching the network. Environment, baselines and analysis are complete; the live "
     "model batch is the next step.</p>"]),
 ],
},
{
 "slug": "penny",
 "num": "02",
 "h1": "Penny — voice-first banking for blind and low-vision customers",
 "nav_title": "Penny",
 "title": "Penny — voice-first accessible banking | Josh Beira",
 "desc": "Voice-first banking for blind and low-vision customers — nothing executes until Penny says what will happen and you confirm it. Barclays Accessibility Challenge.",
 "kicker": "2026 · Barclays Accessibility Challenge",
 "date": "2026-03-01",
 "lead": "Banking for blind and low-vision customers, where voice and sound are the primary channels and the screen is secondary. Nothing executes until Penny says what will happen and you confirm it.",
 "tags": ["TypeScript", "React", "Vite", "Tone.js", "Tesseract.js", "Zustand", "PWA", "Playwright/axe"],
 "langs": ["TypeScript"],
 "repo": "https://github.com/joshbeira/Penny",
 "demo": "https://hey-penny.vercel.app",
 "keywords": ["accessibility", "screen reader", "blind and low vision", "voice interface",
              "sonification", "earcons", "WCAG", "on-device OCR", "progressive web app"],
 "sections": [
   ("designing for sound first, not a screen with labels bolted on",
    ["<p>Most accessible banking is a visual app with ARIA attributes added afterwards. Penny inverts that: "
     "voice and sound are the primary channels and the screen is secondary. It was built for the Barclays "
     "Accessibility Challenge.</p>"]),
   ("the Read-Back Rule",
    ["<p>Nothing executes until Penny states exactly what will happen and is confirmed. For someone who "
     "cannot visually verify a form before submitting it, confirmation has to be spoken, not implied by "
     "what is on screen.</p>",
     "<p>Every completed action writes a hash-chained, tamper-evident receipt, so the history of what was "
     "authorised is checkable after the fact.</p>"]),
   ("Post Box: paper mail without handing it to a server",
    ["<p>Photograph a letter and the sensitive digits are masked on-device with Tesseract before anything "
     "leaves the phone. It is then read back as a summary, verbatim, or explained — and can be acted on in "
     "the same flow, rather than bouncing the user to another part of the app.</p>"]),
   ("Layout Lock: the accessibility contract is enforced by CI",
    ["<p>Layout Lock is a Playwright + axe CI gate that fails the build if the accessibility tree changes "
     "without a migration flag.</p>",
     "<p>The point is that the accessibility contract is enforced by the pipeline, not by remembering. A "
     "refactor that silently reorders the reading order does not ship.</p>"]),
   ("sound carrying information, not just narration",
    ["<p>Account health is a two-second earcon rather than a number, and the week’s spending plays as a "
     "five-second stereo sonification — information conveyed at a glance, for people who do not glance.</p>",
     "<p>Quiet Mode swaps speech for high-contrast cards and three named haptic patterns, for users who "
     "have some vision, or who are simply in public.</p>"]),
   ("it works with no network",
    ["<p>Runs fully offline: no key, no network, no crash. The demo works in airplane mode.</p>"]),
 ],
},
{
 "slug": "byte-the-evidence",
 "num": "03",
 "h1": "Byte the Evidence — an adversarial negotiation trainer for junior M&amp;A lawyers",
 "nav_title": "Byte the Evidence",
 "title": "Byte the Evidence — an M&A negotiation trainer | Josh Beira",
 "desc": "An Ace Attorney-style trainer where junior M&A lawyers negotiate against AI opposing counsel that plants errors and hides facts. 2nd, Legora track, Hack the Law.",
 "kicker": "2026 · Hack the Law, Cambridge — 2nd, Legora track",
 "date": "2026-02-01",
 "lead": "An Ace Attorney-style trainer where junior M&amp;A lawyers negotiate against AI opposing counsel — catching the errors it plants and drawing out the facts it hides, from LOI through to signing.",
 "tags": ["Python", "FastAPI", "Google ADK", "Gemini", "SSE"],
 "langs": ["Python"],
 "repo": "https://github.com/joshbeira/byte-the-evidence-sol2",
 "demo": None,
 "keywords": ["multi-agent systems", "Google ADK", "Gemini", "legal technology",
              "mergers and acquisitions", "LLM agents", "adversarial training", "server-sent events"],
 "sections": [
   ("training the skill, not the fluency",
    ["<p>A junior M&amp;A lawyer’s job in a negotiation is not to sound confident. It is to notice the "
     "clause that is wrong and the fact the other side is not volunteering. Byte the Evidence is built to "
     "train exactly that, across a deal from LOI through to signing. It placed 2nd in the Legora track at "
     "Hack the Law, Cambridge.</p>"]),
   ("four agents behind one session",
    ["<ul><li>A persona-driven negotiator that plants legal errors and guards hidden facts.</li>"
     "<li>An adjudicator scoring every turn.</li>"
     "<li>A phase-boundary coach.</li>"
     "<li>A final evaluator producing per-clause grades and a debrief of everything you missed.</li></ul>",
     "<p>All four are Google ADK agents coordinated behind a single session, so the user experiences one "
     "opponent rather than a pipeline.</p>"]),
   ("the scoring mechanic is the learning objective",
    ["<p>Catching a planted error, or drawing out a fact the other side is hiding, is the scoring mechanic "
     "— so the trainer rewards the actual skill rather than fluency. You cannot score well by writing "
     "confident prose at it.</p>"]),
   ("a demo that could not be broken by an API key",
    ["<p><code>MOCK_LLM=1</code> returns canned responses for the whole agent graph, so the demo never "
     "depended on an API key or a rate limit holding up on the day.</p>"]),
 ],
},
{
 "slug": "lambdagpt",
 "num": "04",
 "h1": "λGPT — a natural-language REPL built from parser combinators, not an LLM",
 "nav_title": "λGPT",
 "title": "λGPT — a natural-language REPL, no LLM | Josh Beira",
 "desc": "A conversational REPL in Haskell with no model behind it — every intent is a Megaparsec parser, every answer is derived, and nothing is generated.",
 "kicker": "2026 · Warwick coursework",
 "date": "2026-01-01",
 "lead": "A conversational interface with no model behind it. Every intent is a parser, every answer is derived, and nothing is generated.",
 "tags": ["Haskell", "Megaparsec", "Aeson", "http-conduit", "Stack"],
 "langs": ["Haskell"],
 "repo": "https://github.com/joshbeira/LambdaGPT",
 "demo": None,
 "keywords": ["Haskell", "parser combinators", "Megaparsec", "functional programming",
              "abstract syntax tree", "REPL", "natural language interface"],
 "sections": [
   ("a conversational interface with nothing generative in it",
    ["<p>λGPT answers questions in natural language without a model anywhere in the loop. Every intent is a "
     "parser, every answer is derived from the input, and nothing is generated. Written in Haskell as "
     "Warwick coursework.</p>"]),
   ("parsing intent with backtracking",
    ["<p>Megaparsec’s <code>try</code> lets the parser backtrack between “what is two plus two” and “what is "
     "the weather like today” without consuming input. <code>string'</code> and <code>optional</code> make it "
     "case-insensitive and tolerant of trailing punctuation, so valid input doesn’t fail on a missing "
     "question mark.</p>"]),
   ("arithmetic over an AST, errors as values",
    ["<p>Arithmetic is evaluated over an AST with a <code>foldl</code> accumulator for left-to-right "
     "natural-language precedence — “two plus three times four” means what a speaker means by it, not what "
     "an algebra parser means.</p>",
     "<p><code>evaluateExpr</code> returns <code>Either String Int</code>, so referencing “that” before any "
     "maths has happened is an error value rather than a runtime crash.</p>"]),
   ("past the spec: a live forecast that cannot take the REPL down",
    ["<p>Went past the spec with a live Open-Meteo forecast, isolated in its own module and fetched with "
     "<code>httpJSONEither</code> — a dropped network returns a polite string instead of killing the REPL. "
     "Keyless by choice, so it can’t fail on someone else’s rate limit.</p>"]),
   ("memory without a monad transformer",
    ["<p>Memory is an explicit association list threaded through the loop by tail recursion rather than a "
     "<code>StateT</code> transformer over IO — less machinery, same guarantee.</p>"]),
 ],
},
{
 "slug": "covid-mortality-risk-model",
 "num": "05",
 "h1": "COVID-19 mortality risk — logistic regression from scratch, and a negative result",
 "nav_title": "COVID-19 mortality risk",
 "title": "COVID-19 mortality risk — a negative result | Josh Beira",
 "desc": "Logistic regression hand-derived in NumPy: 75.82% accuracy against a 75.63% majority-class baseline, and 2.35% recall. A negative result, written up as one.",
 "kicker": "2025",
 "date": "2025-06-01",
 "lead": "Logistic regression written from scratch in NumPy — sigmoid, cross-entropy and hand-derived gradients. It scored 75.82% accuracy against a 75.63% baseline, which is to say it learned almost nothing.",
 "tags": ["Python", "NumPy", "Pandas", "from scratch"],
 "langs": ["Python"],
 "repo": "https://github.com/joshbeira/COVID-Mortality-Risk-Model",
 "demo": None,
 "keywords": ["logistic regression", "NumPy", "gradient descent", "class imbalance",
              "cross-entropy", "negative result", "machine learning from scratch", "model evaluation"],
 "sections": [
   ("written from scratch, on purpose",
    ["<p>No scikit-learn in the model — the cost function and both partial derivatives are hand-derived. "
     "<code>StandardScaler</code> is the only thing borrowed, and only because unscaled age dominates the "
     "gradient and skews the cost surface.</p>"]),
   ("the result",
    ["<p><strong>75.82% accuracy against a 75.63% majority-class baseline.</strong> Recall 2.35%: it found "
     "27 of 1,148 deaths.</p>",
     "<p>Accuracy looks respectable and is almost entirely the baseline. On the metric that matters "
     "clinically, the model had learned almost nothing.</p>"]),
   ("diagnosed rather than buried",
    ["<p>Severe class imbalance, no class weighting, threshold left at 0.5. Written up in the README as "
     "unsuitable for clinical use, because it is.</p>",
     "<p>A model that reports 75.82% accuracy and stops there is a misleading result. The interesting part "
     "of this project is the gap between the number that flatters it and the number that condemns it.</p>"]),
 ],
},
]

import io, os, json, html, datetime
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

def plain(s):  # HTML source string -> plain text for JSON-LD
    return html.unescape(s)

PERSON_STUB = {
    "@type": "Person", "@id": f"{SITE}/#person", "name": "Josh Beira",
    "url": f"{SITE}/",
    "sameAs": ["https://github.com/joshbeira", "https://linkedin.com/in/josh-beira"],
}
WEBSITE_STUB = {
    "@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/",
    "name": "Josh Beira", "inLanguage": "en-GB",
    "publisher": {"@id": f"{SITE}/#person"},
}

def head(title, desc, canonical, extra_ld, og_type="article", published=None):
    article_meta = ""
    if og_type == "article" and published:
        article_meta = (f'\n<meta property="article:published_time" content="{published}">'
                        f'\n<meta property="article:author" content="Josh Beira">')
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="author" content="Josh Beira">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="theme-color" content="#100F0E">
<meta name="color-scheme" content="dark">

<link rel="canonical" href="{canonical}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="{og_type}">{article_meta}
<meta property="og:locale" content="en_GB">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:site_name" content="Josh Beira">
<meta property="og:image" content="{SITE}/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Josh Beira — machine learning and real-time systems">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{SITE}/og.png">

<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="/icon-192.png" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles.css">

<script type="application/ld+json">
{json.dumps(extra_ld, ensure_ascii=False, indent=2)}
</script>
</head>
<body>

<a class="skip" href="#top">Skip to content</a>
<canvas id="bg" class="bg-canvas" aria-hidden="true"></canvas>

<div class="page">

  <header class="site-header">
    <a class="brand" href="/">
      <span class="brand__name">Josh Beira</span>
    </a>
    <nav class="nav" aria-label="Sections">
      <a href="/#experience">experience</a>
      <a href="/work/">work</a>
      <a href="/#education">education</a>
      <a href="/#contact">contact</a>
    </nav>
  </header>
"""

FOOT = """
  <footer class="site-footer">
    <div class="site-footer__inner">
      <span>josh beira · 2026</span>
      <span class="bg-toggle" role="group" aria-label="Background animation">
        <span class="bg-toggle__label">background:</span>
        <button type="button" class="bg-btn is-on" data-bg-mode="lattice" aria-pressed="true">dijkstra</button>
        <span class="bg-toggle__sep" aria-hidden="true">/</span>
        <button type="button" class="bg-btn" data-bg-mode="wavefront" aria-pressed="false">bfs</button>
      </span>
    </div>
  </footer>

</div>

<script src="/scripts/background.js" defer></script>
</body>
</html>
"""

def crumbs(items):
    li = []
    for i, (label, href) in enumerate(items):
        last = i == len(items) - 1
        inner = label if last else f'<a href="{href}">{label}</a>'
        aria = ' aria-current="page"' if last else ''
        li.append(f'        <li{aria}>{inner}</li>')
    return ('    <nav class="crumbs" aria-label="Breadcrumb">\n      <ol>\n'
            + "\n".join(li) + "\n      </ol>\n    </nav>\n")

def crumb_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": plain(label),
         **({"item": SITE + href} if href else {})}
        for i, (label, href) in enumerate(items)]}

# ---------------------------------------------------------------- project pages
for idx, p in enumerate(PROJECTS):
    url = f"{SITE}/work/{p['slug']}/"
    cr = [("josh beira", "/"), ("work", "/work/"), (p["nav_title"], None)]

    ld = {"@context": "https://schema.org", "@graph": [
        PERSON_STUB, WEBSITE_STUB, crumb_ld(cr),
        {"@type": "WebPage", "@id": url + "#webpage", "url": url,
         "name": plain(p["title"]), "description": p["desc"], "inLanguage": "en-GB",
         "isPartOf": {"@id": f"{SITE}/#website"},
         "primaryImageOfPage": f"{SITE}/og.png",
         "about": {"@id": url + "#project"},
         "author": {"@id": f"{SITE}/#person"}},
        {"@type": "SoftwareSourceCode", "@id": url + "#project",
         "name": plain(p["h1"]), "headline": plain(p["h1"]),
         "abstract": plain(p["lead"]), "description": p["desc"],
         "url": url, "codeRepository": p["repo"],
         "programmingLanguage": p["langs"],
         "runtimePlatform": p["tags"],
         "keywords": ", ".join(p["keywords"]),
         "datePublished": p["date"], "inLanguage": "en-GB",
         "author": {"@id": f"{SITE}/#person"},
         "creator": {"@id": f"{SITE}/#person"},
         "isPartOf": {"@id": f"{SITE}/#selected-work"},
         "license": None},
    ]}
    # drop nulls
    ld["@graph"][-1] = {k: v for k, v in ld["@graph"][-1].items() if v is not None}
    if p["demo"]:
        ld["@graph"][-1]["sameAs"] = [p["demo"]]

    body = [head(p["title"], p["desc"], url, ld, published=p["date"]), '\n  <main id="top" class="wrap" tabindex="-1">\n']
    body.append(crumbs(cr))
    body.append('\n    <article class="case">\n')
    body.append(f'      <p class="case__kicker">{p["kicker"]}</p>\n')
    body.append(f'      <h1 class="case__title">{p["h1"]}</h1>\n')
    body.append(f'      <p class="case__lead">{p["lead"]}</p>\n')
    body.append('      <p class="case__tags">'
                + "".join(f'<span class="work-row__tag">{t}</span>' for t in p["tags"])
                + '</p>\n')
    links = [f'<a href="{p["repo"]}" rel="noopener" target="_blank">repo ↗</a>']
    if p["demo"]:
        links.append(f'<a href="{p["demo"]}" rel="noopener" target="_blank">live demo ↗</a>')
    body.append('      <p class="case__links">'
                + '<span class="hero__sep" aria-hidden="true">·</span>'.join(links) + '</p>\n')
    body.append('\n      <div class="case__body">\n')
    for h2, paras in p["sections"]:
        body.append(f'        <h2>{h2}</h2>\n')
        for para in paras:
            body.append(f'        {para}\n')
    body.append('      </div>\n    </article>\n')

    # prev / next keeps every project two clicks from every other one
    prev_p = PROJECTS[idx - 1] if idx > 0 else None
    next_p = PROJECTS[idx + 1] if idx < len(PROJECTS) - 1 else None
    nav = ['\n    <nav class="case-nav" aria-label="More work">\n']
    if prev_p:
        nav.append(f'      <a class="case-nav__prev" href="/work/{prev_p["slug"]}/">'
                   f'<span class="case-nav__dir">← previous</span>'
                   f'<span class="case-nav__name">{prev_p["nav_title"]}</span></a>\n')
    else:
        nav.append('      <span></span>\n')
    if next_p:
        nav.append(f'      <a class="case-nav__next" href="/work/{next_p["slug"]}/">'
                   f'<span class="case-nav__dir">next →</span>'
                   f'<span class="case-nav__name">{next_p["nav_title"]}</span></a>\n')
    nav.append('    </nav>\n')
    nav.append('\n    <p class="case-back"><a href="/work/">all work</a>'
               '<span class="hero__sep" aria-hidden="true">·</span>'
               '<a href="/">josh beira</a></p>\n')
    body.append("".join(nav))
    body.append('\n  </main>\n')
    body.append(FOOT)

    os.makedirs(f"work/{p['slug']}", exist_ok=True)
    io.open(f"work/{p['slug']}/index.html", "w", encoding="utf-8").write("".join(body))
    print(f"  work/{p['slug']}/index.html")

# ------------------------------------------------------------------- work hub
hub_url = f"{SITE}/work/"
hub_title = "Work — machine learning, agents and accessibility | Josh Beira"
hub_desc = ("Five projects by Josh Beira: an agentic trading benchmark, voice-first accessible "
            "banking, a legal negotiation trainer, and a Haskell natural-language REPL.")
hub_cr = [("josh beira", "/"), ("work", None)]
hub_ld = {"@context": "https://schema.org", "@graph": [
    PERSON_STUB, WEBSITE_STUB, crumb_ld(hub_cr),
    {"@type": "CollectionPage", "@id": hub_url + "#webpage", "url": hub_url,
     "name": hub_title, "description": hub_desc, "inLanguage": "en-GB",
     "isPartOf": {"@id": f"{SITE}/#website"},
     "about": {"@id": f"{SITE}/#person"},
     "mainEntity": {"@id": f"{SITE}/#selected-work"}},
    {"@type": "ItemList", "@id": f"{SITE}/#selected-work",
     "name": "Selected work by Josh Beira", "numberOfItems": len(PROJECTS),
     "itemListElement": [
        {"@type": "ListItem", "position": i + 1,
         "url": f"{SITE}/work/{p['slug']}/", "name": plain(p["h1"])}
        for i, p in enumerate(PROJECTS)]},
]}

h = [head(hub_title, hub_desc, hub_url, hub_ld, og_type="website"),
     '\n  <main id="top" class="wrap" tabindex="-1">\n', crumbs(hub_cr),
     '\n    <section class="section section--hub">\n'
     '      <div class="section__head">\n'
     '        <h1>selected work</h1>\n'
     '        <span class="section__rule" aria-hidden="true"></span>\n'
     f'        <span class="section__count">{len(PROJECTS):02d}</span>\n'
     '      </div>\n'
     '      <p class="hub__intro">Machine learning systems built against a constraint — a latency budget, '
     'a user who cannot see the screen, or a benchmark designed to catch me fooling myself. '
     'Each one has a full write-up.</p>\n']
for p in PROJECTS:
    h.append(f'''
      <article class="work-row">
        <span class="work-row__num" aria-hidden="true">{p["num"]}</span>
        <div class="work-row__body">
          <h2 class="work-row__title"><a href="/work/{p["slug"]}/">{p["h1"]}</a></h2>
          <p class="work-row__meta">{p["kicker"]}</p>
          <p class="work-row__summary">{p["lead"]}</p>
          <p class="work-row__tags">{"".join(f'<span class="work-row__tag">{t}</span>' for t in p["tags"])}</p>
          <p class="work-row__links"><a href="/work/{p["slug"]}/">read the write-up →</a></p>
        </div>
      </article>
''')
h.append('      <div class="list-end" aria-hidden="true"></div>\n    </section>\n')
h.append('\n    <p class="case-back"><a href="/">back to josh beira</a></p>\n')
h.append('\n  </main>\n')
h.append(FOOT)
io.open("work/index.html", "w", encoding="utf-8").write("".join(h))
print("  work/index.html")

# --------------------------------------------------------------------- sitemap
today = datetime.date.today().isoformat()
urls = [(f"{SITE}/", today, "monthly", "1.0"), (hub_url, today, "monthly", "0.9")]
urls += [(f"{SITE}/work/{p['slug']}/", today, "yearly", "0.8") for p in PROJECTS]
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for loc, mod, freq, pri in urls:
    sm += ["  <url>", f"    <loc>{loc}</loc>", f"    <lastmod>{mod}</lastmod>",
           f"    <changefreq>{freq}</changefreq>", f"    <priority>{pri}</priority>", "  </url>"]
sm.append("</urlset>")
io.open("sitemap.xml", "w", encoding="utf-8").write("\n".join(sm) + "\n")
print(f"  sitemap.xml ({len(urls)} urls)")
