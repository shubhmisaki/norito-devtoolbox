# Ad network setup guide — Media.net, Ezoic, Carbon Ads

Companion to `ADSENSE_GSC_CHECKLIST.md`. Covers three additional/alternative ad
networks: what each actually requires (not just marketing copy), the signup
steps you do yourself, and the code integration I can do once you have your
account details. None of these can be signed up for on your behalf — account
creation, ownership verification, and payment details are all things only you
can do — but once you have a publisher ID/script snippet, adding it to the
site and deploying it is a five-minute job on this end.

**Honest expectation-setting first:** none of these three has a real "no
bar" approval process despite what a lot of blog-spam guides claim.

- **Media.net** unofficially wants meaningful monthly traffic (guides cite
  ~10K+ uniques as the point where approval odds are decent) and traffic
  weighted toward US/UK/Canada. norito.in has neither yet.
- **Ezoic**'s "Access Now" tier genuinely has no traffic minimum, but it
  serves ads through Google Ad Manager under the hood, so your domain still
  needs Google's approval somewhere in the pipeline — this isn't fully
  independent of Google the way it's sometimes marketed.
- **Carbon Ads** is invite/application-only and explicitly weighs monthly
  pageviews and "is this site actively maintained" in their review.

None of that means don't apply, applying costs nothing but time. Just don't
expect same-week approval at current traffic. Worth doing now so they're
in the pipeline while Show HN / Product Hunt / AlternativeTo bring in real
visitors over the next couple weeks.

---

## 1. Media.net

**What you need before applying:**
- A working email you can verify.
- Ability to add an HTML meta tag or DNS TXT record to prove domain
  ownership (same mechanism as AdSense/GSC verification — Netlify supports
  both).

**Steps (you do this):**
1. Go to [media.net](https://www.media.net/publishers) → "Sign Up."
2. Enter `norito.in`, your email, set a password.
3. Verify domain ownership — pick HTML tag or DNS TXT record. If DNS TXT,
   add it via wherever `norito.in`'s DNS is managed (check if that's
   Netlify DNS or your registrar — if unsure, tell me and I can check the
   Netlify DNS records for the zone).
4. Fill out the site profile (category: tools/utilities, traffic estimate —
   be honest, they can see real numbers via GSC/analytics anyway).
5. Wait — typically 4–7 business days. You'll get an email either way.
6. If approved, your dashboard gives you an ad unit snippet (a `<script>`
   tag plus one or more `<div>` ad slot placements).

**Once you have the snippet (I do this):**
- The script tag goes in `partials/head-common.html` so it loads on all 828
  pages from one edit — this is the correct integration point, unlike how
  AdSense's script currently gets pasted individually into every `src/*.html`
  file (that was the pattern before the partials system covered everything;
  worth migrating AdSense to `head-common.html` too while touching this).
- Ad slot `<div>`s (if Media.net gives you specific placement code rather
  than an Auto-Ads-style script) go into a page-body partial or macro,
  similar to how `<!--RELATED-TOOLS-->` works — tell me where on the page
  you want it to actually appear (below the tool, in the sidebar, etc.) and
  I'll wire it into the templating system rather than hand-editing 640 files.
- `ads.txt` needs a new line for Media.net alongside the existing AdSense
  line — Media.net's dashboard gives you the exact line to add, format is
  usually `media.net, <your-id>, DIRECT`.
- Rebuild (`python3 scripts/build_site.py`), commit, push, same flow as
  everything else this week.

---

## 2. Ezoic

**What you need before applying:**
- Decide on integration method first, this determines the whole setup:
  - **Nameserver integration** (Ezoic's recommended default): you change
    `norito.in`'s nameservers at your registrar to point to Ezoic instead
    of Netlify DNS. Ezoic then proxies all traffic, manages DNS, SSL, and
    injects ads at the edge. This is a bigger structural change — Netlify
    would still build and host the site, but DNS/SSL/CDN would be Ezoic's
    layer in front of it instead of Netlify's. Worth understanding this
    before committing: it changes who's "in front of" the site for every
    request.
  - **Ezoic Cloud (CNAME) integration**: a lighter alternative — a CNAME
    record instead of full nameserver delegation. Less invasive, worth
    asking their support specifically for this if you want to avoid handing
    over full DNS control.
- A Google account (Ezoic ties into Google Ad Manager / MCM on the backend).

**Steps (you do this):**
1. Sign up at [ezoic.com](https://www.ezoic.com) → connect `norito.in`.
2. Choose integration method (nameserver vs. Cloud/CNAME — see above).
3. If nameserver: get the two Ezoic nameservers from the dashboard, update
   them at your domain registrar (wherever `norito.in` is registered — not
   Netlify, registrars are separate from hosts). Propagation takes up to
   18–24 hours.
4. Return to the Ezoic dashboard and confirm "Integration Complete."
5. Ezoic's own review/ramp-up period follows — they gradually enable ad
   serving and test placements via their AI system rather than a single
   pass/fail gate like AdSense.

**Once integration is live (I do this):**
- Ezoic mostly self-manages ad placement after integration (that's the
  point of their AI placement testing), so there's less manual code to add
  compared to Media.net. If they do give you a placeholder script/div for
  specific placements, same approach: goes into `partials/head-common.html`
  or a body partial, not hand-edited per file.
- No `ads.txt` line needed from Ezoic directly in most setups since they
  manage this via their platform, but confirm in their dashboard.

**Given the nameserver commitment, I'd hold off starting this one until
there's real traffic** — worth the DNS change once it's clearly worth the
ad revenue, not before.

---

## 3. Carbon Ads

**What you need before applying:**
- Real traffic numbers to report (pageviews/month) — this is the one where
  applying too early just gets a pass, not a maybe.
- A short description of the site and audience.

**Steps (you do this):**
1. Go to [carbonads.net/join](https://www.carbonads.net/join).
2. Submit `norito.in`, traffic stats, and a short pitch — dev tools,
   privacy-first, no accounts, matches their design/dev-audience network
   well, worth saying so explicitly in the application.
3. Review takes 5–7 business days. They also weigh whether they have open
   capacity in the network right now, not just whether your site qualifies.
4. Payouts go through Open Collective, processed quarterly — worth knowing
   going in, this isn't a fast-cash option even once approved.

**Once approved (I do this):**
- Carbon gives a single small script + one ad unit `<div>` (their format is
  intentionally minimal — one line, small image + text, no banners). Same
  integration approach: script in `partials/head-common.html`, the ad
  `<div>` placed once in a body partial so it's consistent across all tool
  pages in one edit.
- Add their line to `ads.txt` per their dashboard instructions.

---

## Suggested order

1. **Apply to Media.net and Carbon Ads now** — zero cost to apply, and
   having applications in the queue while Show HN/PH/AlternativeTo traffic
   lands means a decision either way arrives faster.
2. **Hold Ezoic** until there's a clearer traffic picture, given the DNS/
   nameserver commitment is bigger than the other two.
3. Whichever comes back approved first, tell me and I'll do the code
   integration the same day — script into `head-common.html`, ad slot into
   the right body partial, `ads.txt` updated, rebuilt, committed, pushed.
