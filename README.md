# norito

63 free, no-signup utilities across PDF, Images, Developer, Text, Utilities,
SEO, and Design categories. Pure HTML/CSS/vanilla JS: no backend for any tool
except where noted, no bundler, no runtime third-party requests. Everything
runs in the visitor's browser, which means free hosting and no server costs.

There *is* a build step, but only for shared chrome, not for tool logic: the
header, footer, and other cross-page boilerplate live once per locale under
`partials/` and get expanded into the live HTML files by
`scripts/build_site.py` (see [Templating](#templating-headerfooter-shared-chrome)
below). Each tool's actual functionality is still one self-contained
`js/app-*.js` file with no bundler or transpile step.

**Tools included** (a representative sample; see `tools.html` or
`partials/en/footer.html` for the full catalog):

| Page | What it does |
| --- | --- |
| `test-file-generator.html` | Generate a file of any size/extension (PDF, ZIP, JPG, PNG, GIF, TXT, BIN), byte-exact. |
| `compress-image.html` | Compress an image to a target file size instead of a quality percentage. |
| `placeholder-generator.html` | Placeholder images with custom size, color, and label text. |
| `password-generator.html` | Random passwords or word-based passphrases, live strength meter. |
| `seo-slug-generator.html` | Clean URL slugs from a title, live, with a batch mode for multiple titles. |
| `limited-text-generator.html` | Generates placeholder text to an exact character count (50/100/250/1000 presets or custom), spaces optional. |
| `json-formatter.html` | Format/validate/minify JSON, collapsible tree view, error line/column. |
| `qr-code-generator.html` | QR codes with custom colors, error correction, optional center logo. |
| `markdown-editor.html` | Split-pane markdown editor with live preview and a formatting toolbar. |
| `remove-background.html` | Cuts a person out of a photo client-side (see caveats below). |
| `color-converter.html`, `contrast-checker.html`, `css-gradient-generator.html` | Design toolkit: HEX/RGB/HSL conversion, WCAG contrast checking, gradient CSS generation. |
| `image-converter.html` | Convert between PNG/JPG/WebP client-side via `canvas.toBlob`. |

62 more tools cover PDF merge/split/rotate/compress, image resizing/cropping,
dev utilities (formatters, encoders, generators), and text tools. Every tool
is one HTML page (for SEO), sharing `css/style.css` and `js/utils.js`.

## Branding

`assets/norito-logo.svg` is the original combined logo, kept for reference.
The header on every page actually renders it as two separate files:
`assets/norito-mark.svg` (mascot) and `assets/norito-wordmark.svg` (text),
so CSS can put real spacing between them; both are crops of the same
artwork, so swapping the original logo means regenerating both crops.
The color palette in `css/style.css` (`--primary`,
`--rose`, `--coral`, `--amber`, `--purple`, `--teal`, `--indigo`) was pulled
directly from the logo's gradient and accent colors. Change those custom
properties to re-theme everything at once.

The blurred pink blobs behind the content (`.bg-blobs` in every page,
driven by `js/bg-blobs.js`) drift subtly toward the cursor on mousemove.
Respects `prefers-reduced-motion`.

## Run it locally

```
python3 -m http.server 8000
```

Then open `http://localhost:8000`. Serving over HTTP (rather than opening
files directly) avoids `file://` restrictions some browsers apply to
`canvas.toBlob` and Web Workers, which several tools rely on.

## Deploy for free

Any static host works:

- **Netlify**: drag the `devtoolbox` folder onto app.netlify.com/drop.
- **Vercel**: `npx vercel` from inside this folder.
- **GitHub Pages**: push to a repo, enable Pages on `main`.
- **Cloudflare Pages**: connect the repo or drag-and-drop.

One thing to check on whichever host you pick: make sure it serves `.wasm`
files with the `application/wasm` content type (all four of the above do by
default), the QR/markdown tools don't need this, but Remove Background
does, since it loads a WebAssembly runtime.

## Vendored dependencies

Everything else in this project is hand-written vanilla JS. A handful of
tools pull in a small MIT/Apache-licensed library, vendored locally (via
`npm install` + copy, not a CDN) so the site has no runtime third-party
requests:

- **QR Code Generator**: `js/vendor/qrcode.js` + `qrcode-utf8.js`,
  kazuhikoarase/qrcode-generator, MIT. ~57KB total.
- **Markdown Editor**: `js/vendor/marked.umd.js`, marked v18, MIT. ~44KB.
- **PDF tools** (merge/split/rotate/etc.): `js/vendor/pdf-lib.min.js`,
  pdf-lib v1.17.1, MIT.
- **PDF to JPG/PNG**: `js/vendor/pdfjs/`, Mozilla's pdf.js
  (pdfjs-dist), Apache 2.0.
- **Remove Background**: `js/vendor/onnxruntime/` (ONNX Runtime Web
  v1.19.2, Microsoft, MIT) + `js/vendor/modnet/` (a quantized MODNet
  portrait-matting model, Apache 2.0). ~18MB combined, downloaded once per
  browser session on first use of the tool, then cached.

See `js/vendor/README.md` for exact versions and provenance.

### Why Remove Background is scoped the way it is

The obvious "best" option for background removal (`@imgly/background-removal`)
was ruled out for two reasons: it's AGPL-licensed (which has real implications
if you monetize this site, you'd need to open-source the codebase or buy a
commercial license), and its realistic payload is 18-30MB (a full ONNX
runtime plus model). The current implementation, ONNX Runtime Web running a
quantized MODNet model, lands in that same 18MB range but under permissive
MIT/Apache 2.0 licenses, no copyleft obligations. The tradeoff is the model
is tuned for photos of people, not general objects or products, and the UI
says so up front rather than overpromising. MODNet does predict a real
per-pixel alpha matte (not just a coarse person/background mask), so hair and
soft edges come out closer to true transparency than a simple segmentation
model would give.

## How the byte-exact file generation works

(`test-file-generator.html` / `js/generators.js`)

- **TXT / BIN**: trivial, filled to the exact byte count.
- **ZIP**: a real ZIP with one stored (uncompressed) entry, sized so the
  total archive matches the target exactly. Verified with `unzip -t`.
- **PDF**: a minimal valid one-page PDF with a padding comment (PDF ignores
  `%` comments), so it opens in any viewer at the exact byte count. Verified
  with `pdfinfo`.
- **GIF**: a real 1×1 GIF with a standard Comment Extension block used as
  padding. Verified by decoding with Pillow.
- **JPG / PNG**: a real tiny generated image, padded using a JPEG COM
  marker segment / a custom ancillary PNG chunk.

A few formats have a small minimum size below which exact padding isn't
possible. The UI always shows the real generated size via `blob.size`,
never just the number you typed in.

`js/test_generators.js` is a Node-based test harness (not loaded by any HTML
page). Run `node js/test_generators.js` if you touch `generators.js`.

## Monetization

**AdSense is wired in.** Every one of the 640 live pages loads the AdSense
Auto Ads script (`ca-pub-4040839176833351`) in `<head>`, and `ads.txt` at
the project root declares the same publisher ID so AdSense can verify the
site. Auto Ads means Google chooses placement and format automatically, no
manual ad-unit divs to maintain across hundreds of pages and 7 languages. If
specific
placements (e.g. only below the lede, never near the dropzone) turn out to
matter, swap Auto Ads for manual `<ins class="adsbygoogle">` units in those
exact spots instead. Utility sites like this tend to do reasonably well with
ads because visitors have high intent and come back repeatedly for the same
tool.

Two things still needed on Google's side before ads actually serve:
account approval for `norito.in` (if not already approved) and Auto Ads
turned on for the site in the AdSense dashboard, the code alone doesn't
serve ads without both.

**Metering free usage + a paid tier is a bigger change.** A pure
client-side counter (localStorage) is trivially bypassed by an incognito
window or clearing storage. It's a soft nudge, not a real limit. A real
paywall needs:

1. Server-side usage tracking tied to some identity (account, or at minimum
   a signed cookie), a couple of Cloudflare Workers or Vercel functions
   would be enough at this scale, no need for a full backend.
2. Payment processing: Stripe Checkout is the standard path, needs one
   endpoint to create a session and one webhook to confirm payment.

This is a separate, smaller project on top of the current site, not a
day-one requirement. Worth doing once you know which tools people actually
use enough to be worth gating. Test File Generator and JSON Formatter are
likely candidates given developer intent, but real usage data beats
guessing.

*(General disclaimer: none of the above is legal or financial advice,
license terms and payment-processing requirements are worth a proper read
or a professional opinion once real money is involved.)*

## SEO notes

Each tool has its own page with a distinct `<title>` (≤60 chars) and `<meta
description>` (≤160 chars) targeting a specific search intent. Every page
also links to every other tool in the footer, which helps each page get
crawled and gives each one some internal link equity. Keep this pattern for
future tools: one page per keyword cluster, not one big app page.

Every page also ships:

- A `rel="canonical"` tag.
- Open Graph and Twitter Card tags, pointing at `assets/og-image.png`
  (1200x630).
- A JSON-LD `WebSite` (index) or `WebApplication` (tool pages) block.
- `sitemap.xml` and `robots.txt` at the project root.

Production domain is `https://norito.in`, used throughout canonical URLs,
Open Graph tags, `sitemap.xml`, and `robots.txt`. If it ever changes, a
project-wide find/replace on `norito.in` covers every reference.

## Localization (7 languages)

The tool catalog ships in seven languages: English at the root
(`index.html`, `compress-image.html`, ...), and full copies under `es/`
(Spanish), `zh/` (Simplified Chinese), `ar/` (Arabic, right-to-left), `hi/`
(Hindi), `ru/` (Russian), and `ja/` (Japanese). That's 640 HTML pages total
across the site, each with its own `<title>`, meta description, canonical
URL, and `hreflang` alternate links pointing at all seven versions plus an
`x-default` fallback to English, so each language ranks as its own page
rather than competing with the others.

**How it's built:** two generations of tooling coexist, since the three
newer locales were added after the original pipeline:

- `i18n/strings.en.json`, `strings.es.json`, `strings.zh.json`,
  `strings.ar.json` are the original source of truth for English/Spanish/
  Chinese/Arabic: one JSON file per language, same key structure, covering
  every static string on every page (`common` = nav/footer/shared bits,
  `pages.<id>` = per-page copy) plus every JS-generated dynamic string
  (`js.<file>`). The `es/`, `zh/`, `ar/` HTML pages were generated from the
  English pages by swapping in these translated strings.
- `hi/`, `ru/`, and `ja/` were added later via the `src/` + `partials/` +
  `scripts/build_site.py` templating system described below instead: each
  locale's page-specific copy lives directly in `src/{locale}/*.html`,
  translated by hand rather than JSON-substituted. There are no
  `i18n/strings.hi.json` / `strings.ru.json` / `strings.ja.json` files, and
  there don't need to be, the templating system's per-locale `src/` and
  `partials/` trees serve the same role for these three locales that the
  JSON files serve for the original three.
- Both mechanisms feed the same runtime layer at the JS level:
  `js/i18n-runtime.js` adds a tiny `i18nFor(fileId)` / `fmt(str, vars)`
  helper, and every `js/app-*.js` file reads its own slice of
  `window.NORITO_I18N` through this, falling back to the English string
  baked into the code if no dictionary is loaded. English pages never load
  a dictionary, so they're unaffected. All six non-English locales load
  `js/i18n/{es,zh,ar,hi,ru,ja}.js` (per-locale runtime dictionaries, one
  file per locale regardless of which pipeline generated that locale's HTML)
  before the tool's own script, which populates `window.NORITO_I18N`.
- If you're adding an eighth locale: prefer the templating path (`src/` +
  `partials/` + `build_site.py`), it's the actively maintained one and
  doesn't require touching the older JSON-substitution scripts, which
  aren't checked in as a live/re-runnable tool (they were a one-time
  generation pass for the original three locales).
- `js/lang-switcher.js` powers the globe-icon menu in the header (present on
  every page). It reads the `hreflang` `<link>` tags already in the page's
  `<head>` and turns them into a dropdown, showing each language in its own
  script (English / Español / 中文 / العربية / हिन्दी / Русский / 日本語) so
  a visitor can find their language without needing to read the current one.
  The dropdown only lists pages that actually exist in a given locale
  (tracked via the `TRANSLATABLE_PAGES` allowlist in that file), falling
  back to the English page otherwise.
- RTL support for Arabic is a `[dir="rtl"]` override block at the bottom of
  `css/style.css`, covering the handful of rules that hardcode a physical
  left/right (nav dropdown position, joined size+unit inputs, toggle switch
  knob, JSON tree indentation, markdown blockquote border, table alignment).
  Everything else is flexbox/grid, which mirrors automatically under
  `dir="rtl"`.
- `sitemap.xml` lists every URL with `xhtml:link` hreflang annotations
  cross-referencing every language version of each page.

**Known limitation:** the SEO Slug Generator's "remove stopwords" option
only recognizes English stopwords ("the", "a", "and"...) on every language
version, since building per-language stopword lists was out of scope for a
string-translation pass. It still works correctly on Spanish/Chinese/Arabic
titles, it just won't strip filler words in those languages.

## Templating (header/footer/shared chrome)

Most pages are no longer edited directly. The header nav, footer, common
`<head>` boilerplate (Clarity, favicons, font preloads), and the shared
foot-of-page scripts (i18n runtime, nav/theme-toggle/lang-switcher, the
command-palette overlay) live once per locale under `partials/`, not
copy-pasted into all 640 HTML files anymore.

- `src/**/*.html` — the editable source for each page: page-specific
  `<title>`/meta/JSON-LD/`<main>` content, with `<!--INCLUDE:...-->` markers
  standing in for the shared chrome.
- `partials/head-common.html` — the `<head>` boilerplate shared by every
  page on the site (one file, no locale variants).
- `partials/{locale}/header.html`, `header-content.html` (used on
  compare/blog pages, which get an extra nav link) — per-locale nav. Same
  fallback rule as the footer: every locale's nav dropdown now lists the
  full 59-tool catalog, using that locale's translated page/label where one
  exists and the English page/label otherwise, so every tool is reachable
  from the nav on every locale (previously each locale's nav only showed
  its ~32 translated tools).
- `partials/{locale}/footer.html` (`footer-home.html` is kept identical, for
  marker compatibility) — one common mega-footer per locale: a full
  Product/PDF/Images/Developer/Text/Utilities/SEO/Design sitemap. Each tool
  link uses that locale's own translated page when one exists (sourced from
  the header partial) and falls back to the English page otherwise — see
  `scripts/build_common_footer.py`. Blog always points to the English
  `/blog/` since it isn't translated yet.
- `partials/{locale}/cmdk-overlay.html` — the Cmd+K search palette markup.
- `<!--RELATED-TOOLS ... -->` — a page-body component macro (not a shared
  partial, since the content is page-specific): a compact `href|label|desc`
  data block per related tool, one per line. `build_site.py` renders it
  into the full "Related tools" card grid, picking the `<h2>` text for the
  page's locale from a fixed 7-locale translation table. Any future styling
  change to the related-tools cards is a one-place edit instead of a
  190-file edit. Extracted via `scripts/extract_related_tools.py`.
- `partials/foot-scripts-head.html`, `foot-scripts-mid.html`,
  `foot-scripts-tail.html` — the shared `<script>` tags around each page's
  own tool-specific script.
- `scripts/build_site.py` — expands `src/` + `partials/` back into the live
  HTML files at the repo root. Run it after editing anything under `src/`
  or `partials/`:

  ```
  python3 scripts/build_site.py
  ```

  It's also wired into `.githooks/pre-commit` (enable once via
  `git config core.hooksPath .githooks`), so a forgotten rebuild before
  commit gets caught and regenerated automatically.

**To change the nav, footer, or any shared chrome for a locale:** edit the
relevant file under `partials/{locale}/`, run the build script once, and
every page in that locale picks up the change — no more hand-editing (or
scripting a find-and-replace across) hundreds of files.

**Coverage:** 639 of 640 pages are on this system, including
`index.html`, `about.html`/`changelog.html`/`contact.html`/`privacy.html`/
`how-it-works.html`/`tools.html`/`404.html`, once the common mega-footer
above replaced their various one-off footer layouts. The only holdout is
`offline.html` (the service-worker offline fallback page), a small
standalone page that doesn't need the shared nav/footer chrome since it's
only ever shown when the visitor has no network connection — see
`scripts/make_src.py` / `scripts/extract_partials.py` for how the rest of
the site was converted, if extending this to cover it too.

## Shared JS helpers (`js/utils.js`)

`js/utils.js` is loaded on every page (via `partials/foot-scripts-head.html`)
before each tool's own `js/app-*.js`. As well as the byte/ZIP helpers, it now
has `copyToClipboard(text)`: tries `navigator.clipboard.writeText`, falls
back to a hidden-textarea `execCommand("copy")` if that's unavailable or
throws. All 26 `app-*.js` files that copy text to the clipboard now call
this instead of duplicating the try/catch inline — which also fixed a real
bug in 8 of them (`app-border-radius-generator.js`, `app-box-shadow-generator.js`,
`app-color-converter.js`, `app-color-palette-extractor.js`,
`app-css-gradient-generator.js`, `app-csv-to-json.js`,
`app-meta-tag-generator.js`, `app-utm-builder.js`) that had no fallback at
all, so the copy button silently did nothing if the Clipboard API was
unavailable (e.g. non-HTTPS contexts, older browsers, permission denied).

`wireDragDrop(el, onDrop)` does the same for the drag-and-drop dropzone
wiring (`dragenter`/`dragover`/`dragleave`/`drop`, `.drag` hover class,
`preventDefault`) that used to be copy-pasted, in one of two equivalent
forms, across `app-*.js` files. 23 of 24 dropzone files now call it;
`app-qrcode.js`'s secondary logo-dropzone was left as-is since it toggles a
different class (`drag-active`) for a distinct, smaller drop target and
isn't worth complicating the shared helper for one file. Converted via
`scripts/consolidate_dropzones.py`; each file's own file-handling logic
(single file, batch, image vs. text) is untouched -- only the
event-wiring boilerplate around it moved into `utils.js`.

## Roadmap

From the original wishlist, still open:

- Fake data generator (names/emails/CSV/JSON).
- A lighter-weight or paid-API path for Remove Background if quality on
  non-portrait photos becomes a real ask.

(Color toolkit and an image converter were both on this list earlier and
have since shipped: see `color-converter.html`, `contrast-checker.html`,
`css-gradient-generator.html`, and `image-converter.html`.)

Each new tool should get its own HTML page and reuse `css/style.css` plus
the existing `js/utils.js` helpers so the codebase stays one shared system
instead of forking per tool.
