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

### 3. Progress feedback is inconsistent across tool categories
The GIF suite (most recently rebuilt) now shows live "Re-encoding... 43%"
progress and a working Cancel button for anything slow. Most of the other
~80 tools — PDF merge/compress, image batch processing, background
removal — show "Reading `<file>`..." and then jump straight to a finished
or failed result, with no feedback during the actual processing step. Per
the Doherty Threshold (Laws of UX: acknowledge any operation that might
run past ~400ms) and NN Heuristic #4 (Consistency and Standards), the
newest corner of the site has quietly set a UX bar the rest doesn't meet.
Worth auditing which non-GIF tools have genuinely slow operations (large
PDFs, big image batches, background removal, PDF-to-image at high
resolution) and wiring the same `onProgress` pattern already proven in
GIF Compressor into those specifically — not all 86 tools need it, most
already resolve in well under a second.

### 4. No undo for destructive in-tool actions
Removing a page in "Delete & Reorder Pages," dropping a frame in a GIF
tool, or clearing a field — the only recovery today is re-uploading the
source file. The UI Patterns library lists Undo as the standard pattern
for exactly this ("Forms → Undo"). A per-tool, session-only undo stack
(not a sitewide feature) would close this for the handful of tools where
users are most likely to remove something by mistake.

### 5. No paste-from-clipboard support
I checked every `js/app-*.js` file for clipboard/paste wiring — none
exists. Every file input is click-to-browse or drag-and-drop only. Pasting
a screenshot or copied image directly (`Ctrl+V`) is now a common
expectation for browser-based image tools and is a clean fit for NN
Heuristic #7 (Flexibility and Efficiency of Use for power users). Scoped
addition to the shared dropzone wiring (`wireDragDrop` already exists as a
shared helper, so this extends one function rather than touching every
tool individually).

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
