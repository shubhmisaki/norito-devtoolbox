# Launch assets — norito.in

Drafts only. Fill in the bracketed spots, read each one over in your own voice before posting, and adjust claims if anything below doesn't match reality by the time you post (traffic-dependent phrasing especially). None of this should go out until the site is live and you've spot-checked it.

## Launch schedule (decided Aug 4, 2026)

Staggered on purpose — same-week launches split attention and traffic, and doing HN first surfaces any bugs/claims issues on a smaller, more technical audience before the bigger PH push.

- **Show HN: Thursday, August 13, 2026, ~8:30 AM ET.** Mid-week, US morning, per HN's own traffic patterns (see notes below). Requires being logged into a Hacker News account with some pre-existing karma/history — brand-new accounts posting Show HN sometimes get flagged. **You'll need to log into HN yourself** (same account-creation rule as DevHunt/AlternativeTo/Uneed applies — I won't do this step).
- **Product Hunt: Tuesday, August 18, 2026, 12:01 AM PT.** One work-week after Show HN, gives time to fix anything HN surfaces first. Tuesday–Thursday are PH's highest-traffic days; launching right at 12:01 AM PT maximizes the full 24-hour voting window. Already logged into Product Hunt in this browser session, so this one's ready to go when the date arrives.
- Repo visibility confirmed: `github.com/ShubhMisaki/norito-devtoolbox` is public and loads normally — the HN post's bracketed caveat about this below has been resolved.

**Tool count note:** the "86" figure below is the verified count of distinct tool pages as of Aug 2026 (counted directly from `tools.html`'s card list, category by category: PDF 12, Images 13, Developer 27, Text 12, Utilities 2, SEO 6, Design 14 = 86). The homepage hero badge currently says "90" — that number is stale/inflated by 4 and should get fixed on-site before or alongside this launch push, so a sharp-eyed commenter counting cards on `tools.html` doesn't catch a mismatch. Re-count before reusing this copy later, the number will drift as tools get added.

## Product Hunt

**Tagline** (60 char max):
> 86 free browser tools. No signup, nothing leaves your device.

**Description:**
> norito is a collection of 86 free utilities that run entirely in your browser: PDF merge/split/compress, image resize/convert/background-removal, JSON/YAML formatters, password and QR generators, text tools, SEO tools, and CSS/design generators.
>
> No account, no watermark, no upload limit. Most tools never send your file anywhere, they process it locally with the Canvas/File/WebAssembly APIs already built into your browser, so a PDF or photo you run through norito never leaves your device. That's not a privacy *policy*, it's checkable: open the Network tab in DevTools while you use one and see for yourself.
>
> Built as one page per tool (not a single do-everything app) so each one loads fast and does one job well. Available in English, Spanish, Chinese, Arabic, Hindi, Russian, and Japanese.

**First comment (post as maker):**
> Hey Product Hunt — built this because I kept hitting paywalls or forced signups for things that are genuinely simple: compress this image, merge these PDFs, generate a QR code. Most of norito runs client-side by design, Remove Background was the one that took the most work to get right, since browser-based background removal without uploading the photo anywhere means running a real ML model (a quantized MODNet) locally via ONNX Runtime Web — about 18MB downloaded once and cached, tuned to stay under permissive MIT/Apache licenses instead of the AGPL-licensed alternative.
>
> Happy to answer questions about how any of it works under the hood. And if a tool you use regularly isn't here, tell me, I'm adding more.

## AlternativeTo

**Description:**
> A collection of 86 free, no-signup browser tools covering PDF (merge, split, compress, rotate, compare), images (resize, convert, compress, background removal, watermark, crop, AVIF/HEIC), developer utilities (JSON/YAML formatters, regex tester, JWT decoder, UUID/hash generators, SVG tools), text tools, SEO utilities, and CSS/design generators. Most tools process files entirely client-side, nothing is uploaded to a server. Free, ad-supported, no account required. Available in 7 languages.

**Suggested "Alternative to" tags** (attach norito as an alternative to the specific tool it competes with, not just a generic category — check each one still applies before submitting):
- Smallpdf, iLovePDF (PDF tools)
- TinyPNG, Squoosh (image compression)
- remove.bg (background removal — the honest caveat: works best on portrait/people photos, not general objects, worth stating up front since remove.bg handles a broader range)
- JSONLint, CyberChef (dev utilities — for the specific formatters, not the whole CyberChef scope)

## Hacker News (Show HN)

**Title:**
> Show HN: norito – 86 free browser tools, most run entirely client-side

**Post body:**
> I built norito, a set of free web utilities (PDF, image, dev, text tools) after getting tired of tools that gate basic features behind signup or a paywall.
>
> The technical bit HN will probably care about most: every tool processes files entirely in the browser, none of them upload anything (verified this by grepping the whole codebase for outbound fetch/XHR calls — the only one that exists loads the WASM runtime binary itself, never user data). Image compression uses canvas.toBlob with a binary-search on quality/dimensions to hit an exact target file size. Background removal runs a quantized MODNet model through ONNX Runtime Web (WASM), fully client-side, about 18MB downloaded once and cached. PDF tools use pdf-lib and pdf.js.
>
> No backend, no database, no server-side file processing at all — every tool runs client-side. It's a static site (Netlify), so hosting cost is close to zero regardless of traffic. Source is at github.com/ShubhMisaki/norito-devtoolbox under MIT.
>
> Feedback on the tools themselves, the "does this actually stay local" claim (you can verify via DevTools Network tab), or the codebase is all welcome.

**Notes for HN specifically:**
- HN is skeptical of "no upload" privacy claims by default — the DevTools-verifiable framing above is intentional, don't soften it into unverifiable marketing language.
- Don't @ mention AdSense/monetization unless asked; if asked directly in comments, answer honestly (ad-supported, no data sold) rather than dodging.
- Post Tuesday–Thursday, US morning (HN traffic patterns), avoid Monday/Friday.

## Reddit (r/webdev, r/SideProject, r/InternetIsBeautiful — check each sub's self-promo rules before posting, some require an X:1 non-self-promo ratio or mod approval first)

**Title:**
> I built 86 free browser tools (PDF, image, dev utilities) that mostly don't touch a server

**Post body:**
> Built this over [actual timeframe — fill in before posting, I don't have a reliable source for how long this took you] — norito.in. It's a static site, one page per tool, most of them process your file entirely client-side (canvas/WASM), so nothing gets uploaded for things like image compression, resizing, or background removal.
>
> No signup, no watermark. Ad-supported instead of paywalled, that's the whole business model, no upsell funnel.
>
> Would genuinely like feedback, especially: (1) any tool that's confusing to use, (2) any tool you wish existed that isn't here yet, (3) any bugs.

---

## Directory submission checklist (lower-effort, ongoing — no single post, just a list to work through)

See `BACKLINKS.md` for the full researched list with real, verified URLs, priority tiers, and per-target notes (what to submit, awesome-list contribution rules, and which directories to skip). Short version:
- **Do first:** the GitHub awesome-lists that genuinely fit (awesome-no-login-web-apps, the awesome-pdf lists, awesome-privacy lists) — open a PR per their contribution guidelines, one line per tool, don't bulk-add.
- **Do next:** DevHunt (dev-tool-specific, free, GitHub-authenticated so it's spam-resistant), AlternativeTo (listing drafted above), Product Hunt / Show HN / Reddit (drafted above).
- **Skip or deprioritize:** the sprawling "indie launch directory" ecosystem (Smol Launch and the dozens of interlinked badge-exchange sites like ufind.best, toolfame.com, findly.tools, Turbo0, Fazier, etc.) — low authority, mostly link to each other, marginal SEO value for the time cost. `BACKLINKS.md` has the reasoning.

Directory submissions and awesome-list PRs are typically fine even before you've built up other backlinks, since they're explicitly built for this. Reddit/HN self-promotion rules are stricter and some subs will remove a post from an account with no prior history, consider participating genuinely in a sub for a bit before posting there.
