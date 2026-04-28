# Gestion Velora — Complete Coverage Plan (SEO + GEO + AI)

Date: 2026-04-28
Target: https://gestionvelora.com
Source reports:
- gestionvelora-full-realestate-2026-04-28.md
- gestionvelora-marketing-2026-04-28.md
- gestionvelora-vs-groupmtl-2026-04-28.md
- gestionvelora-audit-2026-04-28.json

## 1) Current state

- GEO / AI visibility: 90/100 (excellent)
- Passive AI visibility: 88/100 (strong)
- Marketing readiness: 54/100 (moderate)
- AI presence: 45/100 (moderate)
- CRO: 15/100 (needs work)
- Performance: 65/100 (good)

Bottom line:
- Strong technical GEO baseline is already in place.
- Main ranking and conversion upside now comes from content architecture, trust/citation formatting, and conversion UX.
- "Seen by all AI" cannot be guaranteed by any tool; goal is to maximize eligibility and citation probability.

## 2) Highest-priority fixes (next 14 days)

1. Hero above-the-fold value proposition + primary CTA
- Why: CRO and AI extractability both weak at top of page.
- Done when:
  - H1 + one-sentence value proposition visible without scroll (desktop + mobile).
  - One primary CTA button in hero linked to lead form / contact.

2. Add quantified social proof with sources
- Why: 6 unattributed stats found; weak citation trust.
- Done when:
  - Every percentage/number has source + year.
  - Social proof strip added (properties managed, satisfaction, years, etc.) with verifiable source links.

3. Add definition block in first 300 words
- Why: Missing core AI extract pattern for "what is" queries.
- Done when:
  - Homepage includes 1-2 sentence canonical definition of your service in first 300 words.

4. Remove hidden text/cloaking pattern
- Why: Potential trust/citation penalty signal.
- Done when:
  - No meaningful text hidden via `display:none` / `visibility:hidden` on indexable pages.

5. Improve llms.txt linkage + heading anchors
- Why: Largest remaining GEO delta (+4 points potential).
- Done when:
  - llms.txt includes key links: /about, /contact, /services, /pricing, /blog.
  - Main H2/H3 sections have stable `id` anchors on primary pages.

## 3) Content architecture fixes (next 30 days)

1. Comparison pages (high intent)
- Create at least:
  - /velora-vs-groupmtl
  - /velora-vs-gestion-montreal
- Template should include: scope, pricing model, SLA, reporting cadence, compliance handling, ideal client fit.

2. Location pages (local AI + SEO capture)
- Start with top markets:
  - /gestion-immobiliere-montreal
  - /gestion-immobiliere-laval
  - /gestion-immobiliere-longueuil
  - /gestion-immobiliere-brossard
  - /gestion-immobiliere-terrebonne
- Each page must contain unique local proof, local FAQ, and local schema.

3. Email capture / lead magnet
- Add one low-friction offer:
  - "Checklist: How to choose a property manager in Montreal"
- Capture in hero or first two sections.

4. Testimonial and trust blocks
- Add 3+ named testimonials with role/context.
- Add trust/legal badges where valid.

## 4) Technical enhancements (next 30 days)

1. Schema expansion
- Keep LocalBusiness + FAQ.
- Add/validate where relevant:
  - Service schema (bilingual)
  - AggregateRating (only if policy-compliant and real)

2. Media/performance
- Convert images to WebP.
- Reduce render-blocking assets (1 script, 2 stylesheets currently flagged).

3. Deploy generated vertical assets
- Use files from `velora-fixes-v2/vertical/`:
  - real-estate-proptech-trust-page.md
  - property-management-trust-legal-pack.md
  - real-estate-proptech-quote-cta.html
  - schema-service-bilingual.jsonld

## 5) Broader SEO stack (outside GEO-only checks)

These are mandatory to claim "complete" search readiness:

1. Google Search Console diagnostics
- Verify property + sitemaps submitted.
- Index coverage review (excluded, crawled-not-indexed, duplicate canonical).
- Query/page CTR opportunity list (impression-rich, low CTR URLs).

2. Backlink profile and authority gaps
- Audit referring domains, toxic links, and competitor link gap.
- Build backlink targets from associations, local directories, and partner publications.

3. Real Core Web Vitals (field data)
- Pull CrUX/PageSpeed field metrics (mobile priority): LCP, INP, CLS.
- Fix templates failing "Good" thresholds.

4. Server log crawl-depth validation
- Confirm Googlebot and AI citation bots hit money pages.
- Detect orphan pages, crawl traps, low-frequency crawl on target URLs.

## 6) Monitoring cadence

Weekly:
- GEO full report rerun
- Rivalry check vs groupmtl.ca
- Track changes in AI presence and CRO sections

Monthly:
- Search Console trend review
- Backlink delta and lost links report
- Log analysis for crawl depth and bot coverage

## 7) Suggested KPI targets (60 days)

- GEO score: 90 -> 94+
- AI presence: 45 -> 70+
- CRO: 15 -> 55+
- Marketing readiness: 54 -> 75+
- Organic leads from local/service pages: +25%+

## 8) Commands used

```bash
./.venv/bin/geo full https://gestionvelora.com --vertical real-estate-proptech --serp --check-external --output gestionvelora-full-realestate-2026-04-28.md
./.venv/bin/geo marketing https://gestionvelora.com --output gestionvelora-marketing-2026-04-28.md
./.venv/bin/geo rivalry --url https://gestionvelora.com --vs https://groupmtl.ca --vertical real-estate-proptech --market-locale en-fr --output gestionvelora-vs-groupmtl-2026-04-28.md --save-history
./.venv/bin/geo fix --url https://gestionvelora.com --vertical real-estate-proptech --market-locale en-fr --apply --output-dir velora-fixes-v2
./.venv/bin/geo audit --url https://gestionvelora.com --format json --output gestionvelora-audit-2026-04-28.json
./.venv/bin/geo monitor --domain gestionvelora.com
```
