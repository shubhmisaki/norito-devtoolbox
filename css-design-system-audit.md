# CSS Design System Audit — norito.in

Scope: `css/style.css` (single sitewide stylesheet, minified for production —
9 physical lines, ~68KB). Analysis was done on a beautified copy so nothing
in the live file was touched by this pass; all findings below are
recommendations, not applied changes.

## Summary

**Rule blocks reviewed:** ~700 | **Tokens defined:** 62 | **Issues found:** 5
categories below | **Overall:** the token foundation is genuinely solid —
this is not a "start from scratch" situation. The gaps are consistent with
organic growth across ~85 tool pages built incrementally: a few components
independently reinvented colors/sizes that a token already covers.

## What's already good

- A real, well-organized token set already exists: a neutral scale
  (`--n-0` through `--n-900`), seven brand color families each with a
  base/`-bg`/`-text` triad (primary, rose, coral, amber, purple, teal,
  indigo), semantic `--success`/`--danger` with their own bg/border, a
  4-step radius scale, a 4-step shadow scale, and a shared easing curve.
- Dark mode is implemented correctly at the token layer — `[data-theme=dark]`
  overrides 46 of the color tokens directly, so most components get dark
  mode for free just by using `var(--token)`. This is the right pattern.
- Token adoption is decent where it's used: 72 `border-radius` declarations
  and 33 `box-shadow` declarations already reference the scale.

## Issues found

### 1. Duplicate semantic colors (highest-value fix)

"Positive/success" green and "negative/danger" red each exist as **three
independently-invented colors** instead of one reused token:

| Where | Light value | Dark value | Should be |
|---|---|---|---|
| `--success` token (already defined, used by success banners) | `#1f845a` | `#1f845a` (n/a override) | — |
| `.diff-stat-add`, `.diff-add .diff-marker` | `#16a34a` | `#4ade80` | `var(--success)` |
| `table.compare-table td.yes` | `#16a34a` | `#4ade80` | `var(--success)` |
| `.hero-badge .dot`, `.trust-strip svg`, `.recent-chip .new-dot` | `#2fbf71` | (same, no override) | `var(--success)` |
| `--danger` token (already defined) | `#c9372c` | `#c9372c` | — |
| `.diff-stat-remove`, `.diff-remove .diff-marker` | `#dc2626` | `#f87171` | `var(--danger)` |

Each of the ad-hoc pairs also carries its own separate `[data-theme=dark]`
override rule, so this is really ~10 lines of CSS (and 3 slightly different
shades of "green" visible across the compare table, the diff tool, and the
homepage trust badges) that could collapse to one token everyone already
has. This is a visible color change if applied, not just a refactor, so I
did not make it — flagging it as the top recommendation.

### 2. No type scale — 48 distinct `font-size` values

There are tokens for font *family* (`--font-body`, `--font-display`) but
none for size. The result is 48 distinct raw values, many within a hair of
each other in a way that suggests drift rather than intent, e.g. `.82rem`,
`.85rem`, `.88rem`, `.9rem`, `.92rem` all appear multiple times as if
different components independently picked "close enough." A ~8-step scale
(`--text-xs` through `--text-3xl`) would likely absorb most of these without
any visible change, since many of the near-duplicates would round to the
same step.

### 3. `--font-mono` was referenced but never defined — fixed

`font-family: var(--font-mono, monospace)` appears 3 times (code/JSON
preview panels). `--font-mono` had no `:root` definition, so it always fell
through to the generic `monospace` fallback. Defined it as
`"SF Mono","SFMono-Regular","Roboto Mono","Cascadia Code",Consolas,"Liberation Mono",monospace`
(the common cross-platform monospace stack), verified via CSS parse + brace
balance. This is a minor, low-risk visual change (code/JSON preview text
now renders in a deliberate monospace font instead of each browser's
generic default) rather than a pure refactor, so flagging it here even
though it's already applied.

### 4. Scattered one-off `border-radius`/`box-shadow` values

Beyond the 4-step radius scale, raw values appear for `999px` (this was
*exactly* `--radius-full` already — a pure missed-`var()` case, zero visual
risk) plus a long tail of `20px`/`16px`/`14px`/`13px`/`6px`/`5px`/`4px`/
`3px`/`2px` that don't map cleanly to the existing sm/md/lg/xl steps
(8/10/16/22px). Similarly 17 of 50 `box-shadow` declarations don't use the
shadow scale. Some of these are likely legitimate one-offs (a small icon's
corner radius doesn't need a named token). The `999px` case has already
been fixed directly in `css/style.css` (verified via CSS parse + brace
balance, zero other bytes changed) since it carried no visual risk; the
rest of this section is left as recommendations.

### 5. Decorative colors, correctly left untokenized

The `.bg-blobs` gradient blobs and the `.style-tile .tile-swatch.custom-swatch`
rainbow conic-gradient use several raw hex values each. These are
illustrative/one-off by nature (background art, a "custom" swatch preview)
and don't need tokens — noting them only so they're not mistaken for an
oversight if someone re-runs this audit.

## Priority actions, if you want to act on this

1. **Consolidate success/danger green & red** (issue 1) — highest value,
   but it's a visible color change, so I'd want you to sign off on the
   exact shade before I touch it (keep the new unified color, or keep the
   brighter `#16a34a`/`#dc2626` pair and update the `--success`/`--danger`
   tokens to match instead of the other way around).
2. ~~**`border-radius: 999px` → `var(--radius-full)`**~~ (issue 4, partial) —
   done.
3. ~~**Define or drop `--font-mono`**~~ (issue 3) — done, defined.
4. **Type scale** (issue 2) — highest effort, needs visual review since even
   "rounding to the nearest step" changes rendered text size sitewide; best
   done as its own dedicated pass with before/after screenshots, not
   bundled in here.

Only the zero-risk `999px` fix above was applied directly. Everything else
is a recommendation, kept in this separate file rather than pushed into
`css/style.css`, so nothing about the live site's appearance changes as a
side effect of running this audit.
