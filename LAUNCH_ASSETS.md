# Launch assets — norito.in

Drafts only. Fill in the bracketed spots, read each one over in your own voice before posting, and adjust claims if anything below doesn't match reality by the time you post (traffic-dependent phrasing especially). None of this should go out until the site is live and you've spot-checked it.

## Product Hunt

**Tagline** (60 char max):
> 63 free browser tools. No signup, nothing leaves your device.

**Description:**
> norito is a collection of 63 free utilities that run entirely in your browser: PDF merge/split/compress, image resize/convert/background-removal, JSON/YAML formatters, password and QR generators, text tools, and more.
>
> No account, no watermark, no upload limit. Most tools never send your file anywhere, they process it locally with the Canvas/File/WebAssembly APIs already built into your browser, so a PDF or photo you run through norito never leaves your device. That's not a privacy *policy*, it's checkable: open the Network tab in DevTools while you use one and see for yourself.
>
> Built as one page per tool (not a single do-everything app) so each one loads fast and does one job well. Available in English, Spanish, Chinese, Arabic, Hindi, Russian, and Japanese.

**First comment (post as maker):**
> Hey Product Hunt — built this because I kept hitting paywalls or forced signups for things that are genuinely simple: compress this image, merge these PDFs, generate a QR code. Most of norito runs client-side by design, [tool name] was the one that took the most work to get right, since [genuine one-line technical detail — e.g. "browser-based background removal without uploading the photo anywhere means running a real ML model (MODNet) locally via ONNX Runtime Web, which took some tuning to keep the download size reasonable"].
>
> Happy to answer questions about how any of it works under the hood. And if a tool you use regularly isn't here, tell me, I'm adding more.

## AlternativeTo

**Description:**
> A collection of 63 free, no-signup browser tools covering PDF (merge, split, compress, rotate), images (resize, convert, compress, background removal, watermark, crop), developer utilities (JSON/YAML formatters, regex tester, JWT decoder, UUID/hash generators), text tools, and SEO utilities. Most tools process files entirely client-side, nothing is uploaded to a server. Free, ad-supported, no account required. Available in 7 languages.

**Suggested "Alternative to" tags** (attach norito as an alternative to the specific tool it competes with, not just a generic category — check each one still applies before submitting):
- Smallpdf, iLovePDF (PDF tools)
- TinyPNG, Squoosh (image compression)
- remove.bg (background removal — the honest caveat: works best on portrait/people photos, not general objects, worth stating up front since remove.bg handles a broader range)
- JSONLint, CyberChef (dev utilities — for the specific formatters, not the whole CyberChef scope)

## Hacker News (Show HN)

**Title:**
> Show HN: norito – 63 free browser tools, most run entirely client-side

**Post body:**
> I built norito, a set of free web utilities (PDF, image, dev, text tools) after getting tired of tools that gate basic features behind signup or a paywall.
>
> The technical bit HN will probably care about most: every tool processes files entirely in the browser, none of them upload anything (verified this by grepping the whole codebase for outbound fetch/XHR calls — the only one that exists loads the WASM runtime binary itself, never user data). Image compression uses canvas.toBlob with a binary-search on quality/dimensions to hit an exact target file size. Background removal runs a quantized MODNet model through ONNX Runtime Web (WASM), fully client-side, about 18MB downloaded once and cached. PDF tools use pdf-lib and pdf.js.
>
> No backend, no database, no server-side file processing at all — every tool runs client-side. It's a static site (Netlify), so hosting cost is close to zero regardless of traffic. Source is [public/going public shortly] at [GitHub URL] under MIT.
>
> Feedback on the tools themselves, the "does this actually stay local" claim (you can verify via DevTools Network tab), or the codebase is all welcome.

**Notes for HN specifically:**
- HN is skeptical of "no upload" privacy claims by default — the DevTools-verifiable framing above is intentional, don't soften it into unverifiable marketing language.
- Don't @ mention AdSense/monetization unless asked; if asked directly in comments, answer honestly (ad-supported, no data sold) rather than dodging.
- Post Tuesday–Thursday, US morning (HN traffic patterns), avoid Monday/Friday.

## Reddit (r/webdev, r/SideProject, r/InternetIsBeautiful — check each sub's self-promo rules before posting, some require an X:1 non-self-promo ratio or mod approval first)

**Title:**
> I built 63 free browser tools (PDF, image, dev utilities) that mostly don't touch a server

**Post body:**
> Built this over [actual timeframe] — norito.in. It's a static site, one page per tool, most of them process your file entirely client-side (canvas/WASM), so nothing gets uploaded for things like image compression, resizing, or background removal.
>
> No signup, no watermark. Ad-supported instead of paywalled, that's the whole business model, no upsell funnel.
>
> Would genuinely like feedback, especially: (1) any tool that's confusing to use, (2) any tool you wish existed that isn't here yet, (3) any bugs.

---

## Directory submission checklist (lower-effort, ongoing — no single post, just a list to work through)

Each of these usually just needs a submission form, no write-up:
- AlternativeTo (listing drafted above)
- SaaSHub
- ToolFinder / There's An AI For That (only if any tool is meaningfully AI/ML-driven — the background removal tool qualifies, most others don't, don't force-fit)
- Awesome lists on GitHub for relevant categories (e.g. "awesome-pdf", "awesome-developer-tools") — search for these and open a PR adding norito where genuinely relevant, don't spam unrelated lists
- Product directories your specific audience actually uses (e.g. if targeting developers specifically: dev.to "tools I use" style posts, not a directory submission but similar low-effort reach)

Directory submissions and awesome-list PRs are typically fine even before you've built up other backlinks, since they're explicitly built for this. Reddit/HN self-promotion rules are stricter and some subs will remove a post from an account with no prior history, consider participating genuinely in a sub for a bit before posting there.
