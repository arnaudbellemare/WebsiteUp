# Full Audit Report

**URL**: https://gestionvelora.com
**Date**: 2026-04-28
**Vertical**: generic

## Score Summary

| Dimension | Score | Bar | Band |
|-----------|------:|-----|------|
| GEO (AI Visibility) | 90/100 | █████████░ | excellent |
| Marketing Readiness | 54/100 | █████░░░░░ | moderate |
|   Copywriting | 60/100 | ██████░░░░ | good |
|   Content Strategy | 50/100 | █████░░░░░ | moderate |
|   AI Presence | 45/100 | ████░░░░░░ | moderate |
| Conversion (CRO) | 15/100 | █░░░░░░░░░ | needs work |
| Performance | 65/100 | ██████░░░░ | good |

## GEO — AI Visibility

Score: **90/100**

| Category | Score | Max |
|----------|------:|----:|
| Robots | 18 | 18 |
| llms.txt | 14 | 18 |
| Schema | 13 | 16 |
| Meta | 14 | 14 |
| Content | 11 | 12 |
| Signals | 6 | 6 |
| Brand | 8 | 10 |
| AI Disc. | 6 | 6 |

**Recommendations:**

- Keyword stuffing detected: 'management' at 7.1% density — diversify vocabulary
- Hidden text detected (display:none/visibility:hidden with content) — AI crawlers can read it and may penalize this cloaking pattern
- Maintain signal consistency and monitor monthly for trust/citation regressions.
- llms.txt is missing links to important pages: /about, /contact, /services, /pricing, /blog. Add these to the relevant H2 sections so AI systems can discover your key content.
- Add id= attributes to H2/H3 headings to enable section-level citations (currently 0% of headings have anchors). Example: <h2 id="pricing">Pricing</h2>
- 2 of 4 external links carry rel="nofollow". Consider removing nofollow from links to authoritative sources so AI crawlers can follow and validate your citations.

## Copywriting

Score: **60/100**

- ✗ H1: "Gestion immobiliere a Montreal pour coproprietes, location et Airbnb"
- ✗ Value proposition above fold
- ✓ Strong CTAs: Reserve fund for condo in Montreal
- ✓ Benefit language: 100%
- ✓ H2 headings keyword-focused (8/9 with service keywords)

**Issues:**
- No clear value proposition found above the fold

**Suggestions:**
- Add a sub-headline below your H1 that explains the value in one sentence: "[Product] helps [audience] [achieve outcome] without [pain point]." Keep it under 20 words — clarity beats cleverness.

## Images & Visual SEO

Score: **85/100**

- 📷 3 image(s) found
- ✓ Alt text: 3/3 images have alt
- ✓ Keyword alt text: 3/3 mention service/city
- ✓ Keyword filenames: 2/3 match service/city
- ✗ WebP format: 0/3 use WebP
- ✓ Dimensions set (CLS prevention): 3/3

**Issues:**
- No WebP images found — all 3 image(s) use older formats. WebP is 25-35% smaller than JPG/PNG at the same quality.

**Suggestions:**
- Convert all images to WebP using Squoosh.app (free, browser-based) or: cwebp -q 80 input.jpg -o output.webp. Target: hero < 150 KB, section photos < 80 KB, thumbnails < 20 KB.

## Content Strategy

Score: **50/100**

- ✓ Blog (8 articles)
- ✓ FAQ section + FAQPage schema
- ✗ Comparison / alternatives pages
- ✓ Pricing page
- ✗ Email capture / lead magnet
- ✗ Quantified social proof
- ✗ Case studies / success stories
- ✓ Internal links: 326 (need 10+)
- ✓ LocalBusiness schema complete
- ✗ No industry association memberships (trust signals + free backlinks)

**Issues:**
- No comparison or alternatives pages found (/vs/, /compare/, etc.)
- No email capture or lead magnet found
- No quantified social proof found (customer counts, improvement stats)
- No industry association memberships or trust badges detected (BBB, Chambre de commerce, ISO certified, …). These are trust signals and free backlink sources.

**Suggestions:**
- Create at least one '[Your brand] vs [Competitor]' page. These pages are cited in ~33% of AI answers for competitive queries and generate high-intent organic traffic. Key: be fair and structured — AI systems flag obviously biased comparisons.
- Add /pricing.md (plain text file) alongside your pricing page. AI agents evaluating tools on behalf of users can read markdown files directly — no JavaScript rendering required. See ai-seo skill for format guidance.
- Add an email capture with a specific offer: "Free [guide/checklist/audit] for [your audience]." This builds a retargeting list from AI-referred visitors who aren't ready to buy yet. Even a simple newsletter with a clear benefit works.
- Add a numbers bar to your hero or above-fold area: "[X]+ properties managed • [Y]% client satisfaction • [Z]+ years in Montreal." Specific numbers increase AI citation probability by +37% (Princeton GEO study) and significantly improve page conversion.
- Display relevant industry memberships (BBB, Chambre de commerce, ISO certified) — these associations have member directories with free backlinks and are a key trust signal for visitors evaluating your business. Add their logos to your footer or About page.

## AI Presence

Score: **45/100**

- ✓ AI crawlers allowed in robots.txt
- ✗ Definition block in first 300 words
- ✗ 6 unattributed stat(s) — add source citations
- ✓ Server-rendered content
- ✗ Location pages (0 found)
- ✓ Organization sameAs schema

**Issues:**
- No definition block found in first 300 words
- 6 statistic(s) found without source attribution. AI systems deprioritise uncited numbers — they can't verify the source.

**Suggestions:**
- Add a self-contained definition sentence in the first 300 words: "[Your service] is [concise definition in 1-2 sentences]." AI systems pull this verbatim for 'what is X' queries — it's the most-cited content pattern.
- Add source attribution to every statistic: "According to [Source] ([Year]), X%…" or append ([Source], [Year]) after the number. Attributed stats are +37% more likely to be cited by AI search engines (Princeton GEO study).
- Consider creating location-specific pages: /[service]-montreal/, /[service]-laval/, etc. The programmatic-seo Locations playbook shows these pages capture high-intent local queries and each one is an independent AI citation target for '[service] in [city]' searches.

## Media Optimization

Score: **100/100**

- ~ No video or audio found on page.

**Recommendations:**
- No video or audio detected. Adding a product demo video can increase conversion by 20-80%.

## Google First-Page Competitor Analysis

**Keyword**: Gestion immobilière Montréal
**Your word count**: 2731  |  **Competitor avg**: 838  |  **Gap**: 0 words

- 7/10 competitors use schema markup
- 3/10 competitors have FAQ sections
- 2/10 competitors embed video

| # | Domain | Words | H2s | Schema | FAQ |
|---|--------|------:|----:|:------:|:---:|
| 1 | gestionimmobilieremontreal.com | 188 | 4 | ✓ | ✗ |
| 2 | gestion-montreal.com | 824 | 1 | ✗ | ✗ |
| 3 | www.gestionnaireimmobilier.ca | 2401 | — | ✗ | ✗ |
| 4 | immoplex.com | 425 | — | ✓ | ✗ |
| 5 | www.gestioncem.com | 776 | 7 | ✗ | ✗ |
| 6 | gestionltl.ca | 431 | 9 | ✓ | ✗ |
| 7 | groupmtl.ca | 793 | 4 | ✓ | ✓ |
| 8 | www.msimmobiliers.com | 771 | 6 | ✓ | ✗ |
| 9 | summumpm.com | 613 | 13 | ✓ | ✓ |
| 10 | www.gciconstruction.ca | 1164 | 10 | ✓ | ✓ |

**Gaps identified:**
- 7/10 top competitors use structured data schema — schema is a baseline expectation for first-page ranking.

**Location pages to create:**

- `/gestion-immobiliere-montreal-montreal/`
- `/gestion-immobiliere-montreal-laval/`
- `/gestion-immobiliere-montreal-longueuil/`
- `/gestion-immobiliere-montreal-brossard/`
- `/gestion-immobiliere-montreal-boucherville/`
- `/gestion-immobiliere-montreal-repentigny/`
- `/gestion-immobiliere-montreal-terrebonne/`
- `/gestion-immobiliere-montreal-saint-jean-sur-richelieu/`
- `/gestion-immobiliere-montreal-blainville/`
- `/gestion-immobiliere-montreal-mirabel/`
- `/gestion-immobiliere-montreal-mascouche/`
- `/gestion-immobiliere-montreal-chateauguay/`

## Conversion Readiness (CRO)

Score: **15/100**

- ✗ Primary CTA visible above the fold
- ✗ Contact / lead capture form present
- ✓ Phone number / tel: link present
- ✗ Testimonials or social proof section
- ✗ AggregateRating structured data
- ✗ Trust badges / guarantees / certifications

**Priority fixes:**
- Add a prominent action button in the hero section: "Book a free consultation →"
- Embed a short contact form (name, email, message) on the homepage or a linked /contact page.
- Add a "What our clients say" section with 3+ named reviews and star ratings.

## Performance

Score: **65/100**

- Render-blocking scripts: 1
- Render-blocking stylesheets: 2
- Images missing dimensions: 0
- Images missing lazy-load: 0

## Priority Marketing Actions

### 1. Add value proposition sub-headline in hero  [P1]
- **Why**: No clear 'you get X' framing above the fold — visitors must scroll to understand your offer.
- **Impact**: high  |  **Effort**: low
- **Skill**: `copywriting`
- **Estimated lift**: +20-40% scroll depth

### 2. Add quantified social proof (customer count, results stats)  [P1]
- **Why**: Specific numbers boost AI citation probability by +37% and lift conversion. '100+ properties managed' beats 'trusted by many clients'.
- **Impact**: high  |  **Effort**: low
- **Skill**: `copywriting`
- **Estimated lift**: +37% AI citation rate

### 3. Add a definition sentence in the first 300 words  [P1]
- **Why**: AI systems extract '[Service] is [definition]' sentences for 'what is X' queries. Without a definition block, you won't appear for definitional AI Overviews.
- **Impact**: high  |  **Effort**: low
- **Skill**: `ai-seo`
- **Estimated lift**: +AI Overview citations for informational queries

### 4. Create a '[Your brand] vs [Top competitor]' comparison page  [P2]
- **Why**: Comparison content captures 33% of AI citations in competitive queries and drives high-intent visitors already evaluating options.
- **Impact**: high  |  **Effort**: medium
- **Skill**: `competitor-alternatives`
- **Estimated lift**: +30-50% organic AI citations

### 5. Add source attribution to 6 statistic(s)  [P1]
- **Why**: Unattributed numbers are less citable — AI systems can't verify them. 'X% of customers' → 'According to [Source] (2024), X% of customers'.
- **Impact**: medium  |  **Effort**: low
- **Skill**: `ai-seo`
- **Estimated lift**: +37% citation probability per attributed stat

### 6. Create location-specific service pages (/[service]-montreal/, etc.)  [P2]
- **Why**: The programmatic-seo Locations playbook: each service×city page captures '[service] in [city]' searches and is an independent AI citation target.
- **Impact**: medium  |  **Effort**: medium
- **Skill**: `programmatic-seo`
- **Estimated lift**: +local query coverage per city page

### 7. Add email capture / lead magnet  [P3]
- **Why**: AI-referred visitors who aren't ready to book need a lower-commitment offer. A free guide or checklist captures them before they bounce.
- **Impact**: medium  |  **Effort**: medium
- **Skill**: `lead-magnets`
- **Estimated lift**: +10-20% lead capture rate

## GEO Next Actions

- **Improve llms.txt readiness (+4 potential points)** [P1] +4 pts — Improve llms.txt structure (sections, depth, and linked key pages).
- **Improve structured data (+3 potential points)** [P2] +3 pts — Expand JSON-LD coverage with complete, valid business and FAQ schema.
- **Improve entity trust and KG signals (+2 potential points)** [P2] +2 pts — Reinforce entity trust signals with consistent brand, about/contact, and sameAs links.
- **Improve citation-ready content (+1 potential points)** [P3] +1 pts — Hidden text detected (display:none/visibility:hidden with content) — AI crawlers can read it and may penalize this cloaking pattern
