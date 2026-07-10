# norito

Ten free, no-signup utilities. Pure HTML/CSS/vanilla JS: no build step, no
backend for any tool except where noted, no bundler. Everything runs in the
visitor's browser, which means free hosting and no server costs. One HTML
page per tool (for SEO), sharing `css/style.css` and a handful of small JS
helpers.

**Tools included:**

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

Everything else in this project is hand-written vanilla JS. Three tools
pull in a small MIT/Apache-licensed library, vendored locally (via `npm
install` + copy, not a CDN) so the site has no runtime third-party
requests:

- **QR Code Generator**: `js/vendor/qrcode.js` + `qrcode-utf8.js`,
  kazuhikoarase/qrcode-generator, MIT. ~57KB total.
- **Markdown Editor**: `js/vendor/marked.umd.js`, marked v18, MIT. ~44KB.
- **Remove Background**: `js/vendor/mediapipe/`, Google's
  `@mediapipe/selfie_segmentation`, Apache 2.0. ~12MB vendored, but only
  ~5.5MB actually downloads per visitor (one WASM variant + a ~250KB model,
  browser picks SIMD or non-SIMD automatically), cached after first use.

See `js/vendor/README.md` for exact versions and provenance.

### Why Remove Background is scoped the way it is

The obvious "best" option for background removal (`@imgly/background-removal`)
was ruled out for two reasons: it's AGPL-licensed (which has real implications
if you monetize this site, you'd need to open-source the codebase or buy a
commercial license), and its realistic payload is 18-30MB (a full ONNX
runtime plus model), which didn't fit this site's "small, fast utility"
positioning. MediaPipe's selfie segmentation model is Apache 2.0, ~5.5MB,
and battle-tested. The tradeoff is it's tuned for photos of people, not
general objects or products, and the UI says so up front rather than
overpromising.

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

**AdSense is wired in.** Every one of the 44 pages loads the AdSense Auto
Ads script (`ca-pub-4040839176833351`) in `<head>`, and `ads.txt` at the
project root declares the same publisher ID so AdSense can verify the site.
Auto Ads means Google chooses placement and format automatically, no manual
ad-unit divs to maintain across 44 pages and 4 languages. If specific
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

## Localization (Spanish, Chinese, Arabic)

Every one of the 11 tools ships in four languages: English at the root
(`index.html`, `compress-image.html`, ...), and full copies under `es/`,
`zh/` (Simplified Chinese), and `ar/` (Arabic, right-to-left). That's 44
HTML pages total, each with its own `<title>`, meta description, canonical
URL, and `hreflang` alternate links pointing at all four versions plus an
`x-default` fallback to English, so each language ranks as its own page
rather than competing with the others.

**How it's built**, so you can extend it without re-doing the whole thing:

- `i18n/strings.en.json`, `strings.es.json`, `strings.zh.json`,
  `strings.ar.json` are the source of truth: one JSON file per language,
  same key structure, covering every static string on every page (`common`
  = nav/footer/shared bits, `pages.<id>` = per-page copy) plus every
  JS-generated dynamic string (`js.<file>`).
- The localized HTML pages in `es/`, `zh/`, `ar/` are *generated* from the
  English pages by swapping in the translated strings; they aren't
  hand-written. If you edit an English page's copy, the localized versions
  will drift out of sync until regenerated the same way (whitespace-tolerant,
  word-boundary-safe find/replace keyed off `i18n/strings.en.json`, plus a
  fresh JSON-LD block per page). There's no live script checked in for this,
  since it was a one-time generation pass; treat the JSON files as the
  editable source and the HTML files under `es/`/`zh/`/`ar/` as build output.
- `js/i18n-runtime.js` adds a tiny `i18nFor(fileId)` / `fmt(str, vars)`
  helper. Every `js/app-*.js` file reads its own slice of
  `window.NORITO_I18N` through this, falling back to the English string
  baked into the code if no dictionary is loaded. English pages never load
  a dictionary, so they're unaffected. Localized pages load
  `js/i18n/{es,zh,ar}.js` (auto-generated from the `js` section of each
  JSON file) before the tool's own script, which populates
  `window.NORITO_I18N`.
- `js/lang-switcher.js` powers the globe-icon menu in the header (present on
  all 44 pages). It reads the `hreflang` `<link>` tags already in the page's
  `<head>` and turns them into a dropdown, showing each language in its own
  script (English / Español / 中文 / العربية) so a visitor can find their
  language without needing to read the current one.
- RTL support for Arabic is a `[dir="rtl"]` override block at the bottom of
  `css/style.css`, covering the handful of rules that hardcode a physical
  left/right (nav dropdown position, joined size+unit inputs, toggle switch
  knob, JSON tree indentation, markdown blockquote border, table alignment).
  Everything else is flexbox/grid, which mirrors automatically under
  `dir="rtl"`.
- `sitemap.xml` lists all 44 URLs with `xhtml:link` hreflang annotations
  cross-referencing every language version of each page.

**Known limitation:** the SEO Slug Generator's "remove stopwords" option
only recognizes English stopwords ("the", "a", "and"...) on every language
version, since building per-language stopword lists was out of scope for a
string-translation pass. It still works correctly on Spanish/Chinese/Arabic
titles, it just won't strip filler words in those languages.

## Roadmap

From the original wishlist, still open:

- Fake data generator (names/emails/CSV/JSON).
- Color toolkit (palette, contrast checker, HEX↔RGB, gradient generator).
- Image converter (PNG/JPG/WebP): a thin wrapper around `canvas.toBlob`,
  similar to the compressor.
- A lighter-weight or paid-API path for Remove Background if quality on
  non-portrait photos becomes a real ask.

Each new tool should get its own HTML page and reuse `css/style.css` plus
the existing `js/utils.js` helpers so the codebase stays one shared system
instead of forking per tool.
