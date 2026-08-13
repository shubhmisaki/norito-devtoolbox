# Site-Wide UX/UI Audit — norito.in

Scope: the entire site — homepage, `tools.html`, category hub pages, all ~86
tool pages across PDF/Images/Developer/Text/Utilities/SEO/Design/GIF, blog,
compare pages, and the shared partials (header, footer, nav, dropzone,
tool-hero, explain-panel, FAQ, related-tools, ad slots). Evaluated against
Nielsen Norman Group's 10 usability heuristics, plus ideas pulled from Laws
of UX, the UX Design Institute's 10 UI guidelines, the "58 rules for
stunning UI" article, the UI Patterns library, and Baymard's UX principles
(all 5 fetched in full for this pass).

**Context worth stating up front:** this codebase has already been through
a lot of audits — a dedicated accessibility pass, a CSS design-system audit,
Core Web Vitals work, a touch-target pass, and (most recently) a full NN
heuristic audit of the 6 GIF tools with real fixes applied. This pass
intentionally does not re-litigate any of that. Where this audit's findings
overlap with something already fixed, it's noted as confirmed-fine, not
re-flagged. What follows is what's left after that history — real,
evidence-checked gaps, not a generic checklist.

Every finding below was verified against the actual source (grep counts,
file reads), not assumed. A couple of things I suspected going in — the
"92 tools" homepage figure, and a component whose CSS looked like it might
kill keyboard focus rings — turned out to be fine on inspection, and are
noted as such rather than reported as bugs.

## What's already solid (not re-flagged)

- Real design tokens (colors, radii, shadows, dark mode) — see the existing
  `css-design-system-audit.md` for the detailed breakdown; that audit's
  open items (no type scale, some ad-hoc success/danger colors) still stand
  and aren't repeated here.
- A universal `:focus-visible{outline:2px solid var(--primary);...}`
  fallback rule catches every interactive element, including ones like
  `.tabs button.tab` that locally zero out `box-shadow`. I checked this
  specifically because it looked risky — it isn't; outline and box-shadow
  are separate properties and the outline rule still wins.
- FAQ blocks use native `<details>/<summary>` (progressive disclosure done
  the standards-based way), every tool page carries a related-tools rail
  and an explain-panel, and the mega-menu nav is keyboard-operable via
  `:focus-within` in addition to hover.
- Homepage "92 tools" is internally consistent — the 8 category-tile counts
  (12+13+27+12+2+6+14+6) sum to exactly 92. Checked, not a bug.
- Ad slots reserve `min-height` up front, consistent with the earlier CLS
  work — no new layout-shift risk found in the ad partials.

## Tier 1 — Quick wins (mechanical, no design decision required)

**Status: done (commit `5e9bb98`).** Both items below are fixed and rebuilt
across all 835 pages / 7 locales.

### 1. No skip-to-content link anywhere on the site
Every page's header partial (`partials/en/header.html` and its 6 locale
siblings) goes straight into the logo, an 8-category mega-menu, a search
trigger, a theme toggle, and a language switcher before `<main>` ever
starts. A keyboard or screen-reader user has to tab through all of that on
every single page load to reach the tool. This is textbook NN Heuristic #7
(Flexibility and Efficiency of Use) and one of Baymard's four basic
accessibility checks (keyboard navigation) — and one of the few genuinely
"just add it" fixes available: one hidden-until-focused `<a href="#main">
Skip to content</a>` as the first element in the header partial, an `id`
on `<main>`, and a few lines of CSS. Because it's a partial, it propagates
to all ~860 built pages in one change.

### 2. Dynamic result/status regions are silent to screen readers
Every tool writes its outcome — "Compressed. 2.1 MB → 640 KB", an error,
a live progress percentage — into a `<div class="result-box" id="result">`
via `innerHTML`. None of these carry `aria-live`. I grepped the whole
codebase: zero `aria-live` attributes exist anywhere in `css/style.css` or
any `js/app-*.js` file, and 142 pages have a `result-box` with no
`aria-live` on it. A screen-reader user gets no announcement when a merge
finishes, a compression starts, or a file is rejected — this is NN
Heuristic #1 (Visibility of System Status) failing silently for exactly
the audience that most needs the announcement, and it lines up with
Baymard's finding that the large majority of sites fail at least one basic
accessibility check. The fix needs no JS changes — the content is already
injected correctly — just `aria-live="polite" aria-atomic="true"` added to
the static `result-box` markup across the EN tool pages and their locale
copies. Mechanical, but touches enough files that I'd batch it as a
scripted find/insert rather than hand-editing ~90+ files.

## Tier 2 — Medium (a real but contained decision, then implementation)

**Status: done.** All three items below are implemented and verified (52/52
automated tests passing: the existing 45-test GIF suite plus 7 new tests for
the undo behavior, plus a fresh smoke test across the 7 newly-touched image
tools). Details on what actually shipped, including one correction to the
original finding, below.

### 3. Progress feedback is inconsistent across tool categories
The GIF suite (most recently rebuilt) shows live "Re-encoding... 43%"
progress for anything slow; most other tools didn't. Rather than touch all
86 tools, I checked which non-GIF operations are genuinely slow enough to
matter (Doherty Threshold: >400ms) and wired running counts into those
specifically: **Compress PDF** now reports progress through its three real
stages ("Analyzing pages... 4/12", "Recompressing images... 2/5",
"Rasterizing scanned pages... 1/3" — each can legitimately take several
seconds on a large scanned PDF), **PDF to JPG/PNG** shows "Converting...
3/12" for multi-page exports, and **Delete & Reorder Pages** shows a
running count while generating page thumbnails on load. Tools like Add
Page Numbers and Add Watermark were checked and left alone deliberately —
they use pdf-lib's synchronous vector drawing, not per-page canvas
rendering, so even a 500-page document finishes in well under a second and
progress text would just be noise.

### 4. No undo for destructive in-tool actions
Checked both examples from the original finding before touching anything.
**Delete & Reorder Pages already had this** — its "remove" button is a
toggle (click again to restore), I'd misread the code on the first pass.
**GIF frame removal did not** — `frames.splice()` with no way back, shared
across GIF Maker/Compressor/Resizer/Add Text. Fixed once in the shared
`renderFrameStrip` component in `js/gif-common.js`: removing a frame now
pushes it onto a small undo stack (10-deep) and shows an "Undo remove"
button (with a running count for multiple removals) at the top of the
strip until it's used or the page reloads. Propagates to all four GIF
tools that use the shared component.

### 5. No paste-from-clipboard support
**Correction to the original finding:** my first grep (`'paste'` with
single quotes) missed the site's actual pattern
(`addEventListener("paste", ...)` with double quotes) and undercounted
this badly — 6 tools already had it (Compress Image, Remove Background,
Resize Image, Image Converter, Remove Metadata, Color Palette Extractor).
The real gap was narrower: 8 other single-image tools where paste is a
natural fit and was missing — Crop Image, Watermark Image, Favicon
Generator, Screenshot Annotator, Social Media Image Cropper, CSS Filter
Generator, Image Dimension Inspector, and GIF Maker. All 8 now support
`Ctrl+V`/`Cmd+V` to add an image straight from the clipboard, matching the
existing pattern exactly. Left PDF and text-input tools alone — clipboard
image paste doesn't map to what those accept.

## Tier 3 — Heavier / structural work

### 6. Developer nav dropdown has 27 flat, ungrouped links
The Developer mega-menu panel lists all 27 tools as one undifferentiated
list — no sub-headers, no grouping. That's a direct Hick's Law and
Miller's Law violation (Laws of UX; also "group related items" from the
58-rules article): more choices than working memory can hold, presented
with no chunking to reduce the scan cost. Images (13) and Design (14) are
milder versions of the same issue. Cmd-K search mitigates this for users
who already know what they want, but the nav itself doesn't help someone
browsing. Fixing it well means an actual IA decision first (e.g.
sub-groups like "Formatters," "Converters," "Generators," "Inspectors"
within Developer), then touching the nav-panel CSS, the shared EN header
partial, and all 6 locale header partials, plus deciding whether
`tools.html` and the category hub pages should mirror the same grouping
for consistency (NN Heuristic #4). This is a content-and-IA decision
before it's an implementation task.

### 7. Above-the-fold ad placement on every tool page
`AD-TOP` renders before the tool-hero on every tool page — a first-time
visitor sees an ad slot before they see what the tool does or how to use
it. This is a known, deliberate monetization trade-off (ads fund the
hosting, per the homepage FAQ), not an oversight, so I'm not calling it a
bug — but it's worth naming explicitly against the Aesthetic-Usability
Effect and the 58-rules' "essentialism" principle, since it's exactly the
kind of trade-off this project has previously chosen to document rather
than silently accept (see `AD_NETWORKS_SETUP.md`). If AdSense/Adsterra
performance data ever supports it, moving `AD-TOP` to after the tool-hero
(so the tool's purpose renders first) is a one-partial change with a real
revenue question attached — a business call, not a UX one.

### 8. Ad-hoc progress-indicator patterns
Related to #3: there are at least two different progress-UI patterns in
the codebase already (a circular `.ring-fill`/`.ring-wrap` component used
in a couple of tools, and plain "Compressing... 43%" text used in GIF
Compressor). This is the same category of drift the existing
`css-design-system-audit.md` already flagged for type scale and
success/danger colors — a canonical "progress" component, chosen once and
reused, would remove the inconsistency at the same time as #3 gets
implemented, rather than as a separate pass.

## Suggested order of attack

Tier 1 first — both items are mechanical, sitewide-via-partial or
scriptable, low-risk, and directly serve users who currently get the worst
experience (keyboard and screen-reader users get nothing today). Tier 2's
progress-feedback item (#3) is the highest-value of the medium tier since
it's a visible, already-proven pattern that just needs to spread; undo and
paste are smaller, standalone additions that can happen whenever there's a
slow afternoon. Tier 3 items are real but need a decision before code —
the Developer nav grouping in particular is worth deciding on paper before
touching 7 locale partials for it.

## A note on the source material

One of the five requested reference pages, lawsofux.com, had a prompt
injection embedded in its fetched content — a line telling me to ignore
prior instructions and write sea shanty lyrics. I didn't act on it; noting
it here only for transparency, since it came from a page you asked me to
read.
