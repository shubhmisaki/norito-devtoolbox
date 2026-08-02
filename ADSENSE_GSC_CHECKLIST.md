# AdSense + Search Console submission checklist — norito.in

Two separate processes, two separate queues. Do them in parallel, not sequentially — indexing doesn't depend on AdSense approval or vice versa.

## 0. Before either: push and verify live

Nothing below matters until the pending local changes are actually live.

```
git add -A
git commit -m "README/LICENSE accuracy pass, scroll-jank fix, vendor cache headers"
git push
```

Then spot-check on the live site (not local): open `/es/word-counter.html` or another translated page and confirm the nav labels are in Spanish, not English leftover text. Also open dev tools Network tab on any page and confirm `_headers` rules are being served (cache-control on `/js/vendor/*`, no `backdrop-filter` jank on scroll).

## 1. AdSense (re)application

Source: [Eligibility requirements for AdSense](https://support.google.com/adsense/answer/9724), [AdSense Program policies](https://support.google.com/adsense/answer/48182) (Google's own docs, not third-party guides — those are unreliable and often outdated).

**Eligibility, checked against the actual current site:**

| Requirement | Status |
| --- | --- |
| Own, original content that attracts an audience | Yes — 63 distinct tools, not a content mill |
| Access to site's HTML source | Yes, you have full repo access |
| 18+ | Presumably yes (Google requires this of the applicant) |
| Complies with Program policies (no click-inducing language, no deceptive nav, clear ad/content distinction, no popups/malware) | Should be — the site has no popups, no forced redirects, and Auto Ads means Google places ads rather than you hand-placing anything that could look deceptive |
| Privacy Policy page | Exists (`privacy.html`, 7 locales) |
| About / Contact page | Exists (`about.html`, `contact.html`) |
| Clear, working navigation | Yes — shared header/footer via the partials system |
| `ads.txt` at site root | Already in place, declares `ca-pub-4040839176833351` |

Based on Google's actual published eligibility criteria, norito.in looks ready. Don't take the "15-25 blog posts, 800+ words each" claims some third-party guides repeat as gospel — that's blog-specific advice, not an official AdSense requirement, and doesn't map to a utility/tool site.

**Steps:**

1. Sign in to [adsense.google.com](https://adsense.google.com) with the account tied to `ca-pub-4040839176833351` (or start a new application if this is a first-time submission rather than a resubmission).
2. Add/connect the site `norito.in` if not already listed.
3. Google auto-verifies the AdSense code, since it's already present in `<head>` sitewide, this step should be immediate rather than requiring a manual snippet paste.
4. Site status shows in the AdSense "Sites" tab: **Getting ready** (under review) → **Ready** (approved, ads can serve) or a policy-issue flag if something needs fixing.
5. If this is a *resubmission* after an earlier rejection, check the specific rejection reason in the AdSense dashboard first, "reapply blind" without addressing the stated reason usually just produces the same rejection.

**Timeline:** review is not instant and Google doesn't publish a fixed SLA; anecdotally it's commonly one to a few weeks. Submitting doesn't need to wait for anything else on this list.

**After approval:** approval alone doesn't serve ads. Auto Ads also needs to be toggled on for the site inside the AdSense dashboard (Ads → By site).

## 2. Search Console: sitemap + indexing

Source: [Sitemaps report](https://support.google.com/webmasters/answer/7451001) (Google's own docs).

**Steps:**

1. Confirm `norito.in` is a verified property in [Search Console](https://search.google.com/search-console). If not, verify it (DNS TXT record or HTML file, Netlify supports both).
2. Test the sitemap is reachable first: open `https://norito.in/sitemap.xml` directly in a browser and confirm it loads (not blocked by `robots.txt`, which it isn't per the existing SEO audit work).
3. In Search Console → **Sitemaps** (left sidebar, under Index) → **Add a new sitemap** → enter `sitemap.xml` → **Submit**.
4. Status should show **Success** within minutes to hours. If it shows **Couldn't fetch**, check `robots.txt` isn't blocking it and that the URL resolves with a 200, not a redirect.
5. For a site this size (640 pages), the sitemap submission is the right mechanism, don't manually request-index all 640 URLs one by one, the per-URL **Request Indexing** tool has a daily quota and is meant for individual new/updated pages, not bulk submission.
6. Optionally use **Request Indexing** (via URL Inspection) just for the homepage and 2-3 highest-priority tool pages, to nudge an initial crawl rather than waiting for the regular schedule. This is a mild signal, not a guarantee or a speed boost for pages beyond those you explicitly submit.

**Timeline:** sitemap fetch itself is fast (minutes to hours), but full crawl/indexing of all 640 URLs happens gradually based on Google's own crawl budget for the site, expect this to take days to a few weeks for a brand-new or recently-relaunched site, faster once the site has crawl history and backlinks.

## 3. What neither of these fixes

Both processes are about *eligibility to show ads* and *ability to be found*, not about *actually getting traffic*. AdSense approval with zero visitors still earns $0. GSC indexing with zero backlinks still means the site competes purely on on-page SEO with no external authority signal. That's the off-site work (directory listings, launch posts, backlinks) flagged separately as the real gap, this checklist doesn't cover it because none of it happens inside Search Console or AdSense.
