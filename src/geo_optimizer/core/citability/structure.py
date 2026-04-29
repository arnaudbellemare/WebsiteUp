"""Citability: structural content analysis functions.

Covers: answer-first structure, passage density, readability, FAQ detection,
format mix, snippet readiness, chunk quotability, blog structure,
answer capsule detection.
"""

from __future__ import annotations

import functools
import json
import re

from geo_optimizer.models.results import MethodScore
from geo_optimizer.core.citability._helpers import _get_clean_text

# ─── Shared regex used across multiple functions ──────────────────────────────

# Pattern for concrete facts: numbers, percentages, assertive statements
_FACT_RE = re.compile(
    r"\b\d+(?:\.\d+)?%"  # percentages
    r"|\$\d+"  # currency
    r"|\b\d{2,}\b"  # numbers with 2+ digits
    r"|\b(?:is|are|was|were|has|have|can|will|must|should"
    r"|è|sono|ha|hanno|può|deve)\b",  # assertive verbs EN+IT
    re.IGNORECASE,
)

# Pattern for citable facts: numbers, dates, specific claims (NO IGNORECASE)
_CITABLE_FACT_NUMERIC_RE = re.compile(
    r"\b\d+(?:\.\d+)?%"  # percentages
    r"|\$\d+(?:[.,]\d+)*"  # currency $
    r"|€\d+(?:[.,]\d+)*"  # currency €
    r"|\b\d{4}\b"  # years
    r"|\b\d+(?:\.\d+)?\s*(?:million|billion|thousand|miliardi|milioni)\b"  # large numbers
    r"|\b\d+(?:\.\d+)?\s*(?:x|times|volte)\b",  # multipliers
    re.IGNORECASE,
)

# Regex: sentence-ending punctuation (period, question mark, exclamation)
_SENTENCE_END_RE = re.compile(r"[.!?](?:\s|$)")

# Explicit definitions in first 150 chars after a heading
_SNIPPET_DEF_RE = re.compile(
    r"\b(?:is|are|refers?\s+to|means?|can\s+be\s+defined\s+as"
    r"|è|sono|si\s+riferisce\s+a|significa)\b",
    re.IGNORECASE,
)


# ─── 10. Answer-First Structure (+25%) — AutoGEO ICLR 2026 ───────────────────


def detect_answer_first(soup) -> MethodScore:
    """Detect answer-first structure: H2 followed by paragraph with concrete fact.

    AutoGEO (ICLR 2026) identifies AnswerFirst as one of the most effective
    strategies for AI citation. For each H2, checks if the first paragraph
    contains a concrete fact (number, assertive statement) in the first 150 chars.
    """
    h2_tags = soup.find_all("h2")
    if not h2_tags:
        return MethodScore(name="answer_first", label="Answer-First Structure", max_score=5, impact="+25%")

    answer_first_count = 0
    for h2 in h2_tags:
        # Fix #400: find the first text after H2 in p, div, li (WordPress/Elementor wraps
        # content in <div><p>...</p></div>, so direct sibling <p> is not always present)
        next_el = h2.find_next(["p", "div", "li"])
        if not next_el:
            continue
        # Skip empty elements (empty divs without text content)
        first_text = next_el.get_text(strip=True)[:150]
        if not first_text:
            continue
        if _FACT_RE.search(first_text):
            answer_first_count += 1

    total_h2 = len(h2_tags)
    ratio = answer_first_count / total_h2 if total_h2 > 0 else 0

    # Score proportional to the percentage of H2s with answer-first
    score = min(int(ratio * 8), 5)

    return MethodScore(
        name="answer_first",
        label="Answer-First Structure",
        detected=ratio >= 0.3,
        score=score,
        max_score=5,
        impact="+25%",
        details={
            "h2_count": total_h2,
            "answer_first_count": answer_first_count,
            "ratio": round(ratio, 2),
        },
    )


# ─── 11. Passage Density (+23%) — Stanford Nature Communications 2025 ────────


def detect_passage_density(soup) -> MethodScore:
    """Detect self-contained dense passages (50-150 words with numeric data).

    Stanford Nature Communications 2025: paragraphs of 50-150 words containing
    concrete data have 2.3x citation rate compared to generic paragraphs.
    """
    paragraphs = soup.find_all("p")
    if not paragraphs:
        return MethodScore(name="passage_density", label="Passage Density", max_score=5, impact="+23%")

    total_paras = 0
    dense_paras = 0

    for p in paragraphs:
        text = p.get_text(strip=True)
        word_count = len(text.split())
        if word_count < 10:
            # Paragraphs that are too short are skipped
            continue
        total_paras += 1
        # Dense paragraph: 50-150 words with at least one numeric data point
        if 50 <= word_count <= 150 and re.search(r"\b\d+(?:\.\d+)?[%$€]?|\b\d{3,}\b", text):
            dense_paras += 1

    ratio = dense_paras / total_paras if total_paras > 0 else 0

    # Score proportional to the percentage of dense paragraphs
    score = min(int(ratio * 10), 5)

    return MethodScore(
        name="passage_density",
        label="Passage Density",
        detected=dense_paras >= 2,
        score=score,
        max_score=5,
        impact="+23%",
        details={
            "total_paragraphs": total_paras,
            "dense_paragraphs": dense_paras,
            "ratio": round(ratio, 2),
        },
    )


# ─── 12. Readability Score (+15%) — SE Ranking 2025 ───────────────────────────


@functools.lru_cache(maxsize=512)
def _count_syllables(word: str) -> int:
    """Approximate syllable count for English/Italian words (cached)."""
    word = word.lower().strip()
    if len(word) <= 3:
        return 1
    # Count vowel groups as an approximation
    vowels = "aeiouyàèéìòùü"
    count = 0
    prev_vowel = False
    for ch in word:
        is_vowel = ch in vowels
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    # At least 1 syllable
    return max(count, 1)


def detect_readability(soup, clean_text: str | None = None) -> MethodScore:
    """Detect readability using Flesch-Kincaid Grade Level and section length."""
    body_text = clean_text or _get_clean_text(soup)
    words = body_text.split()
    if len(words) < 30:
        return MethodScore(name="readability", label="Readability Score", max_score=8, impact="+15%")

    # Count sentences
    sentences = [s.strip() for s in re.split(r"[.!?]+", body_text) if len(s.strip().split()) >= 3]
    num_sentences = max(len(sentences), 1)
    num_words = len(words)

    # Count total syllables
    total_syllables = sum(_count_syllables(w) for w in words)

    # Flesch-Kincaid Grade Level
    fk_grade = 0.39 * (num_words / num_sentences) + 11.8 * (total_syllables / num_words) - 15.59

    # Check section length between headings
    headings = soup.find_all(["h1", "h2", "h3", "h4"])
    section_lengths = []
    for _i, h in enumerate(headings):
        # Count words between this heading and the next
        section_text = []
        sibling = h.find_next_sibling()
        while sibling and sibling.name not in ["h1", "h2", "h3", "h4"]:
            if sibling.name in ["p", "li", "td"]:
                section_text.append(sibling.get_text(strip=True))
            sibling = sibling.find_next_sibling()
        section_word_count = len(" ".join(section_text).split())
        if section_word_count > 0:
            section_lengths.append(section_word_count)

    # Sections with optimal length (100-150 words)
    optimal_sections = sum(1 for sl in section_lengths if 100 <= sl <= 150) if section_lengths else 0
    section_ratio = optimal_sections / max(len(section_lengths), 1)

    # Score calculation
    score = 0

    # Sweet spot Grade 6-8: maximum AI citations
    if 6 <= fk_grade <= 8:
        score += 5
    elif 5 <= fk_grade <= 10:
        score += 3
    elif 4 <= fk_grade <= 12:
        score += 1

    # Bonus for sections with optimal length
    score += min(int(section_ratio * 3), 3)

    return MethodScore(
        name="readability",
        label="Readability Score",
        detected=6 <= fk_grade <= 10,
        score=min(score, 8),
        max_score=8,
        impact="+15%",
        details={
            "flesch_kincaid_grade": round(fk_grade, 1),
            "avg_words_per_sentence": round(num_words / num_sentences, 1),
            "avg_syllables_per_word": round(total_syllables / num_words, 2),
            "optimal_sections": optimal_sections,
            "total_sections": len(section_lengths),
        },
    )


# ─── 13. FAQ-in-Content Check (+12%) — SE Ranking 2025 ───────────────────────


def detect_faq_in_content(soup) -> MethodScore:
    """Detect FAQ patterns in content (not FAQPage schema, which has zero impact)."""
    faq_count = 0

    # Pattern 1: heading ending with "?" followed by a paragraph
    for heading in soup.find_all(["h2", "h3", "h4"]):
        heading_text = heading.get_text(strip=True)
        if heading_text.endswith("?"):
            # Look for an answer paragraph after the heading
            next_elem = heading.find_next_sibling()
            if next_elem and next_elem.name in ["p", "div", "ul", "ol"]:
                answer_text = next_elem.get_text(strip=True)
                if len(answer_text) >= 20:
                    faq_count += 1

    # Pattern 2: <details><summary> FAQ pattern
    details_elements = soup.find_all("details")
    for detail in details_elements:
        summary = detail.find("summary")
        if summary:
            summary_text = summary.get_text(strip=True)
            # Verify there is content after the summary
            detail_text = detail.get_text(strip=True).replace(summary_text, "").strip()
            if len(detail_text) >= 20:
                faq_count += 1

    # Pattern 3: dt/dd (definition list come FAQ)
    dt_elements = soup.find_all("dt")
    for dt in dt_elements:
        dd = dt.find_next_sibling("dd")
        if dd and "?" in dt.get_text():
            faq_count += 1

    # Score based on the number of FAQ patterns found
    if faq_count >= 5:
        score = 6
    elif faq_count >= 3:
        score = 4
    elif faq_count >= 1:
        score = 2
    else:
        score = 0

    return MethodScore(
        name="faq_in_content",
        label="FAQ-in-Content",
        detected=faq_count >= 1,
        score=min(score, 6),
        max_score=6,
        impact="+12%",
        details={
            "faq_patterns_found": faq_count,
        },
    )


# ─── 18. Response Format Mix (+8%) ───────────────────────────────────────────


def detect_format_mix(soup) -> MethodScore:
    """Detect mix of content formats: paragraphs, lists, tables."""
    has_paragraphs = len(soup.find_all("p")) >= 3
    has_lists = len(soup.find_all(["ul", "ol"])) >= 1
    has_tables = len(soup.find_all("table")) >= 1

    # Additional formats (bonus)
    has_code = len(soup.find_all(["pre", "code"])) >= 1
    has_blockquote = len(soup.find_all("blockquote")) >= 1

    # Count formats present
    base_formats = sum([has_paragraphs, has_lists, has_tables])
    bonus_formats = sum([has_code, has_blockquote])

    # Score: full if all 3 base formats are present
    if base_formats == 3:
        score = 4 + min(bonus_formats, 1)  # max 5
    elif base_formats == 2:
        score = 2 + min(bonus_formats, 1)  # max 3
    elif base_formats == 1:
        score = 1
    else:
        score = 0

    return MethodScore(
        name="format_mix",
        label="Response Format Mix",
        detected=base_formats >= 2,
        score=min(score, 5),
        max_score=5,
        impact="+8%",
        details={
            "has_paragraphs": has_paragraphs,
            "has_lists": has_lists,
            "has_tables": has_tables,
            "has_code": has_code,
            "has_blockquote": has_blockquote,
            "format_count": base_formats + bonus_formats,
        },
    )


# ─── 26. Snippet-Ready / Zero-Click (#249) ────────────────────────────────────


def detect_snippet_ready(soup) -> MethodScore:
    """Detect zero-click / snippet-ready content sections.

    Checks if headings are followed by concise definitions (first 150 chars)
    or if question headings (ending with '?') have direct answers under 60 words.
    """
    headings = soup.find_all(["h2", "h3", "h4"])
    if not headings:
        return MethodScore(name="snippet_ready", label="Snippet-Ready Content", max_score=4, impact="+10%")

    snippet_ready_count = 0

    for heading in headings:
        heading_text = heading.get_text(strip=True)
        # Find the first paragraph after the heading
        next_p = heading.find_next("p")
        if not next_p:
            continue
        p_text = next_p.get_text(strip=True)

        # Pattern 1: heading with "?" → direct answer under 60 words
        if heading_text.endswith("?"):
            word_count = len(p_text.split())
            if 5 <= word_count <= 60:
                snippet_ready_count += 1
                continue

        # Pattern 2: explicit definition in the first 150 chars after heading
        first_150 = p_text[:150]
        if _SNIPPET_DEF_RE.search(first_150):
            snippet_ready_count += 1

    total_headings = len(headings)
    ratio = snippet_ready_count / total_headings if total_headings > 0 else 0

    # Proportional score
    if ratio >= 0.5:
        score = 4
    elif ratio >= 0.3:
        score = 3
    elif ratio >= 0.15:
        score = 2
    elif snippet_ready_count >= 1:
        score = 1
    else:
        score = 0

    return MethodScore(
        name="snippet_ready",
        label="Snippet-Ready Content",
        detected=snippet_ready_count >= 1,
        score=min(score, 4),
        max_score=4,
        impact="+10%",
        details={
            "snippet_ready_sections": snippet_ready_count,
            "total_headings": total_headings,
            "ratio": round(ratio, 2),
        },
    )


# ─── 27. Chunk Quotability (#229) ────────────────────────────────────────────


def detect_chunk_quotability(soup) -> MethodScore:
    """Detect quotable content chunks: self-contained paragraphs with concrete data.

    For each paragraph of 50-150 words, checks if it contains concrete data
    (numbers, percentages, dates) making it independently quotable by AI.
    """
    paragraphs = soup.find_all("p")
    if not paragraphs:
        return MethodScore(name="chunk_quotability", label="Chunk Quotability", max_score=4, impact="+10%")

    candidate_count = 0
    quotable_count = 0

    for p in paragraphs:
        text = p.get_text(strip=True)
        word_count = len(text.split())
        # Only paragraphs in the 50-150 word range
        if word_count < 50 or word_count > 150:
            continue
        candidate_count += 1
        # Verify concrete data
        if _CITABLE_FACT_NUMERIC_RE.search(text):  # fix #7: unified regex
            quotable_count += 1

    ratio = quotable_count / candidate_count if candidate_count > 0 else 0

    # Score proportional to the % of quotable paragraphs
    if ratio >= 0.5:
        score = 4
    elif ratio >= 0.3:
        score = 3
    elif ratio >= 0.15:
        score = 2
    elif quotable_count >= 1:
        score = 1
    else:
        score = 0

    return MethodScore(
        name="chunk_quotability",
        label="Chunk Quotability",
        detected=quotable_count >= 1,
        score=min(score, 4),
        max_score=4,
        impact="+10%",
        details={
            "candidate_paragraphs": candidate_count,
            "quotable_paragraphs": quotable_count,
            "ratio": round(ratio, 2),
        },
    )


# ─── 28. Blog Structure (#230) ───────────────────────────────────────────────


def detect_blog_structure(soup) -> MethodScore:
    """Detect blog structure signals in Article/BlogPosting schema.

    Checks: datePublished/dateModified, author bio, categories/tags.
    Only scores if Article or BlogPosting schema is present (non-blog pages get 0).
    """
    # Look for Article or BlogPosting schema in JSON-LD
    article_schema = None
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string or "")
            items = data if isinstance(data, list) else [data]
            for item in items:
                if isinstance(item, dict):
                    schema_type = item.get("@type", "")
                    types = schema_type if isinstance(schema_type, list) else [schema_type]
                    if any(t in ("Article", "BlogPosting", "NewsArticle") for t in types):
                        article_schema = item
                        break
        except (json.JSONDecodeError, TypeError):
            continue
        if article_schema:
            break

    # If no Article/BlogPosting schema, score 0 without penalty
    if not article_schema:
        return MethodScore(
            name="blog_structure",
            label="Blog Structure",
            detected=False,
            score=0,
            max_score=4,
            impact="+8%",
            details={"has_article_schema": False},
        )

    score = 0
    has_dates = bool(article_schema.get("datePublished") or article_schema.get("dateModified"))
    has_author = bool(article_schema.get("author"))
    # Look for categories/tags in meta tags or schema
    has_categories = bool(
        article_schema.get("articleSection")
        or article_schema.get("keywords")
        or soup.find("meta", attrs={"property": "article:tag"})
    )
    # Look for author bio in the DOM
    author_bio = soup.find_all(
        ["div", "section", "aside"],
        class_=re.compile(r"author|bio|about-author|byline", re.I),
    )
    has_author_bio = bool(author_bio)

    if has_dates:
        score += 1
    if has_author:
        score += 1
    if has_author_bio:
        score += 1
    if has_categories:
        score += 1

    return MethodScore(
        name="blog_structure",
        label="Blog Structure",
        detected=score >= 2,
        score=min(score, 4),
        max_score=4,
        impact="+8%",
        details={
            "has_article_schema": True,
            "has_dates": has_dates,
            "has_author": has_author,
            "has_author_bio": has_author_bio,
            "has_categories": has_categories,
        },
    )


# ─── Answer Capsule Detection (#372) ─────────────────────────────────────────


def detect_answer_capsule(soup, clean_text: str | None = None) -> MethodScore:
    """Detect self-contained answer paragraphs extractable by RAG systems (#372).

    An answer capsule is a paragraph that:
    1. Starts with a direct statement (not a question or transition)
    2. Contains a concrete fact (number, name, date)
    3. Is 30-120 words (fits in a single RAG chunk)
    4. Ends with a complete sentence (not truncated)
    """
    paragraphs = soup.find_all("p")
    if not paragraphs:
        return MethodScore(
            name="answer_capsule",
            label="Answer Capsule Detection",
            max_score=4,
            impact="+12%",
        )

    capsule_count = 0
    total_candidates = 0

    for p in paragraphs:
        text = p.get_text(strip=True)
        words = text.split()
        word_count = len(words)

        # Only paragraphs in the 30-120 word range (RAG chunk sweet spot)
        if word_count < 30 or word_count > 120:
            continue
        total_candidates += 1

        # Must end with sentence-ending punctuation
        if not _SENTENCE_END_RE.search(text[-3:]):
            continue

        # Must contain a concrete fact (number, percentage, date, proper noun)
        if not _CITABLE_FACT_NUMERIC_RE.search(text):
            continue

        # Must start with a direct statement (not a question or weak opener)
        first_word = words[0].lower().rstrip(",:")
        if first_word in (
            "however",
            "but",
            "although",
            "moreover",
            "furthermore",
            "additionally",
            "nevertheless",
            "meanwhile",
        ):
            continue

        capsule_count += 1

    ratio = capsule_count / total_candidates if total_candidates > 0 else 0

    if ratio >= 0.4:
        score = 4
    elif ratio >= 0.25:
        score = 3
    elif ratio >= 0.15:
        score = 2
    elif capsule_count >= 1:
        score = 1
    else:
        score = 0

    return MethodScore(
        name="answer_capsule",
        label="Answer Capsule Detection",
        detected=capsule_count >= 2,
        score=min(score, 4),
        max_score=4,
        impact="+12%",
        details={
            "capsule_count": capsule_count,
            "total_candidates": total_candidates,
            "ratio": round(ratio, 2),
        },
    )
