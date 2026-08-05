# Backlink targets — norito.in

Researched Aug 2026. Every link below was fetched or searched directly, not guessed from training data — but re-verify before submitting since these things drift (repos archive, directories shut down, submission rules change). Priority order reflects link value vs. effort, not just what's easiest.

## Tier 1 — GitHub awesome-lists (best value: real audiences, durable dofollow links, one-time PR)

Contribute via pull request per each repo's own contributing guide. One line per tool, matching their existing entry format exactly. Don't bulk-add several norito tools to the same list in one PR unless the list is clearly organized to expect that — a single well-placed entry beats a PR that reads as spam.

**General "no login required" tools**
- [aviaryan/awesome-no-login-web-apps](https://github.com/aviaryan/awesome-no-login-web-apps) — 3.2k stars, 325 forks, actively maintained, CC0 licensed, has a `CONTRIBUTING.md`. Organized by tool category (Drawing, File Converters, Programming Tools, Text tools, etc.) rather than by product, so it fits single tools better than a "norito" entry — pick 1–2 standout pages (e.g. the QR generator, or a PDF tool under a new/existing PDF-adjacent section) rather than trying to list the whole site once.

**PDF-specific**
- [karllhughes/awesome-pdf](https://github.com/karllhughes/awesome-pdf) — has a dedicated Tools/Converters/Services section, good fit for the PDF suite.
- [abhi18av/awesome-pdf](https://github.com/abhi18av/awesome-pdf) — already lists browser-based all-in-one PDF tools as a category, direct fit.
- [OneOffTech/awesome-pdf](https://github.com/OneOffTech/awesome-pdf) — leans toward self-hosted/open tools (e.g. Stirling-PDF); check their framing before submitting since norito isn't self-hosted, but "runs entirely client-side" is an adjacent enough pitch.
- [py-pdf/awesome-pdf](https://github.com/py-pdf/awesome-pdf) — more library/API-focused (fpdf2, pdflatex); weaker fit, lower priority.

**CSS/SVG-specific** (fits the Design category: gradient, shadow, filter, clamp, easing, pattern, blob, noise-texture generators)
- [awesome-css-group/awesome-css](https://github.com/awesome-css-group/awesome-css) — confirmed they already list individual CSS generator tools (e.g. a glassmorphism generator), so single-generator entries are accepted, not just frameworks/libraries.
- [uhub/awesome-css](https://github.com/uhub/awesome-css) — broader CSS list, check their tools section.
- [willianjusten/awesome-svg](https://github.com/willianjusten/awesome-svg) — README explicitly invites contributions; fits the SVG optimizer, sprite generator, and SVG-to-React tools.

**Privacy-focused developer tools** (fits the "nothing leaves your device" pitch specifically)
- [Lissy93/awesome-privacy](https://github.com/Lissy93/awesome-privacy) — established, comprehensive privacy-tool list.
- [iAnonymous3000/awesome-privacy-tools](https://github.com/iAnonymous3000/awesome-privacy-tools) — same space, separate maintainer, worth a separate submission.

**General free/dev tools**
- [t18n/awesome-dev-tools](https://github.com/t18n/awesome-dev-tools)
- [mathewlewallen/awesome-free-tools](https://github.com/mathewlewallen/awesome-free-tools)

### Explicitly skip

- **septimlabs-code/awesome-privacy-devtools** — surfaced in search as a seemingly on-topic match ("developer tools that don't send your data to a server"), but on inspection it's not a genuine community list: 0 stars/forks/watchers, every single linked tool routes to the maintainer's own commercial products (septimforge.vercel.app, septimlabs.vercel.app) with paid tiers, and the README embeds an active "flash sale — expires midnight ET" pitch. It also cites a specific "JSON Formatter Chrome extension adware incident" as its origin story, which reads as a manufactured hook rather than a real, checkable event. Submitting here gets norito zero real audience and associates it with what looks like a self-promotional/SEO operation, not a curated resource. Don't submit.
- **ripienaar/free-for-dev** — huge, legitimately well-known (frequently cited), but its scope is free tiers of *hosted* SaaS/PaaS/IaaS (databases, monitoring, CI, etc.), not client-side browser tools. Wrong category, would likely get the PR closed.

## Tier 2 — Launch/discovery directories (real audiences, one submission each)

- **[Product Hunt](https://www.producthunt.com)** — copy drafted in `LAUNCH_ASSETS.md`. Biggest single-day audience, one-shot — pick the day carefully (see notes in that file).
- **[DevHunt](https://devhunt.org)** — Product Hunt specifically for developer tools, launched 2023 by an indie builder frustrated that PH under-serves dev tools. Free, requires GitHub auth to submit (which cuts down on spam and means it's a real developer audience, not a link farm). Strong fit for norito's Developer category tools specifically.
- **[AlternativeTo](https://alternativeto.net)** — copy drafted in `LAUNCH_ASSETS.md`. Submit norito as an alternative to Smallpdf, iLovePDF, TinyPNG, remove.bg, JSONLint per-tool, not as one generic listing.
- **[Hacker News (Show HN)](https://news.ycombinator.com)** — copy drafted in `LAUNCH_ASSETS.md`.
- **[Uneed](https://www.uneed.best)** — free submission for indie/bootstrapped tools; free tier doesn't get a dofollow link (that's reserved for paid placement), so treat this as discovery traffic rather than an SEO play.
- **Launching Next** — one of the older startup directories, low traffic now but free, permanent, dofollow, and takes five minutes. Low effort justifies including it even though it won't move the needle much on its own.

## Tier 3 — Deprioritize / skip

While researching directories I ran into a large, tightly interlinked web of "indie launch" sites: Smol Launch and roughly twenty others it cross-promotes with badge exchanges (ufind.best, toolfame.com, saasfame.com, findly.tools, Turbo0, Fazier, StartupTrusted, Good AI Tools, LaunchDirectories, SaaSBison, DodoDirectory, Huzzler, Indie.Deals, LaunchVault, Roozna, ToolPilot AI, Web Review, Toolfio, SumoDir, Twelve Tools). Smol Launch's own footer displays roughly 20 of these "Featured on X" badges linking to each other — that mutual-badge pattern is a strong signal these mostly transfer authority to each other rather than to genuinely high-traffic destinations, and burning an afternoon submitting to all of them has a low expected return relative to one solid PR to a 3k-star awesome-list. Not worth the time unless you're specifically doing a broad-spectrum SEO push later and want the long tail — if so, Smol Launch itself (free tier, weekly cohort, permanent dofollow listing after badge verification) is the one worth doing first since the rest largely feed off it.

## Before submitting anywhere

The homepage currently claims "90 tools" but the actual card count on `tools.html` is 86 (see the note at the top of `LAUNCH_ASSETS.md`). Fix that sitewide first — an inflated headline number is exactly the kind of thing a skeptical HN or awesome-list reviewer will check.

## Ready-to-submit PR content

Fetched each repo's actual `README.md` to match their exact entry format and section placement rather than guessing. For the four below, this is submit-ready as-is (still read it over once in your own voice first). Workflow for each: fork → edit `README.md` → add the one line in the spot noted → commit → open PR with the title/description given.

### 1. karllhughes/awesome-pdf

Add as a new bullet at the **end of the `## Tools` section**, right after the existing `hushvert` entry and before the `### Converters` subsection starts. Matches the format of the two entries already there (PDF Toolbox, hushvert) almost exactly in positioning — client-side, no-upload PDF tools.

```markdown
- [norito](https://norito.in/pdf/) - Free browser-based PDF tools: merge, split, compress, rotate, sign, watermark, extract text, and compare two PDFs. All client-side via pdf-lib and pdf.js, no file uploads.
```

- **PR title:** Add norito to Tools
- **PR description:** Adding norito's PDF suite (merge/split/compress/rotate/sign/watermark/extract/compare) — free, client-side, no uploads, fits alongside the PDF Toolbox and hushvert entries already in this section.

### 2. abhi18av/awesome-pdf

Add as a new bullet under **`## Online PDF Tools`**, after the PDFGem entry. That section already lists AllInOneTools, Fluranto, MiOffice, and PDFGem — all privacy-first, client-side, no-signup PDF tool suites, so this is a direct match. Note this section's recent entries use an en dash (`–`) not a hyphen.

```markdown
- [norito](https://norito.in/pdf/) – Free browser-based PDF tools (merge, split, compress, rotate, sign, watermark, compare) plus 70+ other utilities. Client-side via pdf-lib/pdf.js, no uploads, no sign-up.
```

- **PR title:** Add norito to Online PDF Tools
- **PR description:** Adding norito, a client-side PDF toolkit (merge/split/compress/rotate/sign/watermark/compare) — fits alongside the other privacy-first browser tools already listed in this section.

### 3. awesome-css-group/awesome-css

Add as a new bullet under **`## Miscellaneous`**, alphabetically between "Live editor for CSS and LESS" and "RevengeCSS" (the section is roughly alphabetized by title). Uses `*` bullets, not `-`, in this file — match that.

```markdown
* [norito CSS Tools](https://norito.in/design/) - Free CSS generators: gradients, box-shadow, border-radius, clamp(), easing curves, filters, tileable patterns, blob shapes, and noise textures. Copy the CSS, nothing uploaded.
```

- **PR title:** Add norito CSS Tools to Miscellaneous
- **PR description:** Adding norito's CSS generator suite — fits alongside the Glassmorphism Generator and GradientArt entries already in this section.

### 4. aviaryan/awesome-no-login-web-apps

This list is organized by single-purpose tool, and the closest existing precedent for a multi-tool site is the `freetools.site` entry under `### Utilities (uncategorized)` ("Free online tools. Convert or edit documents, images, audio, video and more."). Add right after it.

```markdown
- [norito](https://norito.in/) - 86 free browser tools (PDF, image, dev, text, SEO, and CSS/design utilities). Every tool runs entirely client-side, nothing is uploaded.
```

- **PR title:** Add norito to Utilities
- **PR description:** Adding norito, a collection of 86 free browser-only tools — similar positioning to the freetools.site entry already listed here, everything runs client-side with no uploads.

### Not drafted — check manually first

- **willianjusten/awesome-svg** and **Lissy93/awesome-privacy** — I couldn't fetch either repo's actual README content (both came back empty on `master` and `main`), so I don't have their real entry format to match. Open each repo directly, check `CONTRIBUTING.md` if present, and match the existing formatting by hand before adding an SVG-tools or privacy-tools entry for norito.
- **OneOffTech/awesome-pdf**, **py-pdf/awesome-pdf**, **uhub/awesome-css**, **t18n/awesome-dev-tools**, **mathewlewallen/awesome-free-tools**, **iAnonymous3000/awesome-privacy-tools** — same story, not yet fetched for exact format. Worth doing once the four above are submitted and you want to keep going.
