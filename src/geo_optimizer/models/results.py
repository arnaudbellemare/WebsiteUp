"""
Dataclasses for GEO Optimizer results.

All audit functions return these structures instead of printing.
The CLI layer is responsible for formatting and display.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

# ─── HTTP cache ───────────────────────────────────────────────────────────────


@dataclass
class CachedResponse:
    """Synthetic HTTP response built from the on-disk cache (fix #83).

    Used by run_full_audit() when use_cache=True and the response
    is already in the FileCache, avoiding a new HTTP request.
    """

    status_code: int
    text: str
    content: bytes
    headers: dict[str, str] = field(default_factory=dict)


# ─── Robots.txt ──────────────────────────────────────────────────────────────


@dataclass
class RobotsResult:
    found: bool = False
    bots_allowed: list[str] = field(default_factory=list)
    bots_missing: list[str] = field(default_factory=list)
    bots_blocked: list[str] = field(default_factory=list)
    # Partially blocked bots (Disallow: / + specific Allows — #106)
    bots_partial: list[str] = field(default_factory=list)
    citation_bots_ok: bool = False
    # True if citation bots are explicitly allowed (not just via wildcard — #111)
    citation_bots_explicit: bool = False


# ─── llms.txt ────────────────────────────────────────────────────────────────


@dataclass
class LlmsTxtResult:
    found: bool = False
    has_h1: bool = False
    has_description: bool = False  # alias for has_blockquote, kept for API backward compatibility
    has_sections: bool = False
    has_links: bool = False
    word_count: int = 0
    has_full: bool = False  # /llms-full.txt present
    # #247: llms.txt Policy Intelligence — content analysis
    sections_count: int = 0
    links_count: int = 0
    # #39: llms.txt v2 validation — full spec conformance
    has_blockquote: bool = False  # > blockquote description present
    has_optional_section: bool = False  # ## Optional section present
    companion_files_hint: bool = False  # link to companion .md files
    validation_warnings: list[str] = field(default_factory=list)  # conformance warnings
    # Coverage quality: are important pages (about, services, pricing…) linked?
    coverage_score: int = 0  # 0-100
    important_pages_linked: list[str] = field(default_factory=list)
    important_pages_missing: list[str] = field(default_factory=list)


# ─── Schema JSON-LD ──────────────────────────────────────────────────────────


@dataclass
class SchemaResult:
    found_types: list[str] = field(default_factory=list)
    has_website: bool = False
    has_webapp: bool = False
    has_faq: bool = False
    has_article: bool = False
    has_organization: bool = False
    has_howto: bool = False
    has_person: bool = False
    has_product: bool = False
    raw_schemas: list[dict] = field(default_factory=list)
    any_schema_found: bool = False  # True if ANY valid JSON-LD was found
    has_sameas: bool = False  # sameAs property found
    sameas_urls: list[str] = field(default_factory=list)
    has_date_modified: bool = False  # dateModified in any schema
    # Schema richness (Growth Marshal Feb 2026): schema con 5+ attributi rilevanti
    schema_richness_score: int = 0
    avg_attributes_per_schema: float = 0.0
    # #232: E-commerce GEO Profile — analisi ricchezza Product schema
    ecommerce_signals: dict = field(default_factory=dict)
    # Fix #399: conteggio errori di parsing JSON-LD
    json_parse_errors: int = 0
    # WebApplication on a non-app site triggers Rich Result validation errors
    webapp_invalid: bool = False  # True when WebApplication + no tool/calculator signals


# ─── Meta tags ───────────────────────────────────────────────────────────────


@dataclass
class MetaResult:
    has_title: bool = False
    has_description: bool = False
    has_canonical: bool = False
    has_og_title: bool = False
    has_og_description: bool = False
    has_og_image: bool = False
    title_text: str = ""
    description_text: str = ""
    description_length: int = 0
    title_length: int = 0
    canonical_url: str = ""


# ─── Content quality ─────────────────────────────────────────────────────────


@dataclass
class ContentResult:
    has_h1: bool = False
    heading_count: int = 0
    has_numbers: bool = False
    has_links: bool = False
    word_count: int = 0
    h1_text: str = ""
    numbers_count: int = 0
    external_links_count: int = 0
    has_heading_hierarchy: bool = False  # H2+H3 present in correct hierarchy
    has_lists_or_tables: bool = False  # <ul>/<ol>/<table> found
    has_front_loading: bool = False  # key info in the first 30%
    # Stable anchors: headings with id= for section-level citations
    headings_with_id: int = 0
    heading_id_ratio: float = 0.0  # fraction of h2/h3 with id attribute
    # Definition-first: opening paragraph answers the topic in 1-3 sentences
    has_definition_first: bool = False
    # Text-to-HTML ratio: visible text bytes / raw HTML bytes (0.0–1.0)
    text_html_ratio: float = 0.0
    # External links with rel="nofollow" on the <a> tag
    external_nofollow_count: int = 0
    all_external_nofollow: bool = False  # True when every outgoing external link is nofollowed


# ─── Signals tecnici (v4.0) ──────────────────────────────────────────────────


@dataclass
class SignalsResult:
    """Technical signals for AI discoverability."""

    has_lang: bool = False
    lang_value: str = ""
    has_rss: bool = False
    rss_url: str = ""
    has_freshness: bool = False
    freshness_date: str = ""


# ─── Brand & Entity (v4.3) ────────────────────────────────────────────────────


@dataclass
class BrandEntityResult:
    """Brand and entity identity signals for AI perception."""

    # Entity Coherence (3 points)
    brand_name_consistent: bool = False
    names_found: list[str] = field(default_factory=list)
    schema_desc_matches_meta: bool = False

    # Knowledge Graph Readiness (3 points)
    kg_pillar_count: int = 0
    kg_pillar_urls: list[str] = field(default_factory=list)
    has_wikipedia: bool = False
    has_wikidata: bool = False
    has_linkedin: bool = False
    has_crunchbase: bool = False

    # About/Contact Signals (2 points)
    has_about_link: bool = False
    has_contact_info: bool = False  # Organization with address/telephone/email or Person with jobTitle

    # Geographic Identity (1 point)
    has_geo_schema: bool = False  # address/areaServed/LocalBusiness
    has_hreflang: bool = False
    hreflang_count: int = 0

    # Topic Authority (1 point)
    faq_depth: int = 0  # number of FAQs in the FAQPage schema
    has_recent_articles: bool = False  # Article/BlogPosting with dateModified


# ─── Citability (Princeton GEO Methods) ─────────────────────────────────────


@dataclass
class MethodScore:
    """Score for a single Princeton GEO method."""

    name: str  # "cite_sources"
    label: str  # "Cite Sources"
    detected: bool = False
    score: int = 0
    max_score: int = 10
    impact: str = ""  # "+27%"
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class CitabilityResult:
    """Citability analysis result with the 9 Princeton KDD 2024 methods."""

    methods: list[MethodScore] = field(default_factory=list)
    total_score: int = 0  # 0-100 (normalized sum)
    grade: str = "low"  # low/medium/high/excellent
    top_improvements: list[str] = field(default_factory=list)


# ─── AI Discovery (geo-checklist.dev) ────────────────────────────────────────


@dataclass
class AiDiscoveryResult:
    """Result of checking AI discovery endpoints (.well-known/ai.txt, /ai/*.json)."""

    has_well_known_ai: bool = False
    has_summary: bool = False
    has_faq: bool = False
    has_service: bool = False
    summary_valid: bool = False  # ha i campi richiesti (name + description)
    faq_count: int = 0  # number of FAQs found
    endpoints_found: int = 0  # total count of endpoints found (0-4)


# ─── CDN AI Crawler Check (#225) ─────────────────────────────────────────────


@dataclass
class CdnAiCrawlerResult:
    """Result of checking if CDN blocks AI crawler user-agents.

    Simulates requests as AI bots (GPTBot, ClaudeBot, PerplexityBot) and
    compares status codes + content-length to a normal browser request.
    """

    checked: bool = False
    browser_status: int = 0
    browser_content_length: int = 0
    bot_results: list[dict] = field(default_factory=list)
    # bot_results: [{"bot": "GPTBot", "status": 200, "content_length": 12345,
    #                "blocked": False, "challenge_detected": False}]
    any_blocked: bool = False
    cdn_detected: str = ""  # "cloudflare", "akamai", "aws", "" if none
    cdn_headers: dict[str, str] = field(default_factory=dict)
    error: str = ""  # fix #304: error message (unsafe URL, timeout, etc.)


# ─── JS Rendering Check (#226) ──────────────────────────────────────────────


@dataclass
class JsRenderingResult:
    """Result of checking if page content is accessible without JavaScript.

    Analyzes raw HTML (no JS execution) for content indicators:
    word count, heading count, SPA framework detection.
    """

    checked: bool = False
    raw_word_count: int = 0
    raw_heading_count: int = 0
    has_empty_root: bool = False  # <div id="root"></div> or id="app"
    has_noscript_content: bool = False
    framework_detected: str = ""  # "react", "vue", "angular", "next", ""
    js_dependent: bool = False  # True if content likely needs JS
    details: str = ""


# ─── WebMCP Readiness Check (#233) ────────────────────────────────────────────


@dataclass
class WebMcpResult:
    """Checks whether the site is ready for AI agents via WebMCP and related signals."""

    checked: bool = False

    # WebMCP detection
    has_register_tool: bool = False  # navigator.modelContext.registerTool()
    has_tool_attributes: bool = False  # HTML attributes toolname/tooldescription
    tool_count: int = 0  # number of declared tools

    # Agent-readiness signals
    has_potential_action: bool = False  # schema potentialAction (SearchAction, etc.)
    potential_actions: list[str] = field(default_factory=list)  # action types found
    has_labeled_forms: bool = False  # forms with accessible label + description
    labeled_forms_count: int = 0
    has_openapi: bool = False  # link to OpenAPI/Swagger spec

    # Summary
    agent_ready: bool = False  # True if at least 1 WebMCP signal or 2+ agent-readiness signals
    readiness_level: str = "none"  # "none", "basic", "ready", "advanced"


# ─── Prompt Injection Detection (#276) ────────────────────────────────────────


@dataclass
class PromptInjectionResult:
    """Detection of prompt injection patterns in web content (v4.4)."""

    checked: bool = False

    # Cat 1: text hidden via inline CSS
    hidden_text_found: bool = False
    hidden_text_count: int = 0
    hidden_text_samples: list[str] = field(default_factory=list)

    # Cat 2: invisible Unicode characters
    invisible_unicode_found: bool = False
    invisible_unicode_count: int = 0

    # Cat 3: direct LLM instructions
    llm_instruction_found: bool = False
    llm_instruction_count: int = 0
    llm_instruction_samples: list[str] = field(default_factory=list)

    # Cat 4: prompt in HTML comments
    html_comment_injection_found: bool = False
    html_comment_injection_count: int = 0
    html_comment_samples: list[str] = field(default_factory=list)

    # Cat 5: monochrome text (color ≈ background)
    monochrome_text_found: bool = False
    monochrome_text_count: int = 0

    # Cat 6: micro-font injection (font-size < 2px)
    microfont_found: bool = False
    microfont_count: int = 0

    # Cat 7: data attribute injection (data-ai-*, data-prompt-*)
    data_attr_injection_found: bool = False
    data_attr_injection_count: int = 0
    data_attr_samples: list[str] = field(default_factory=list)

    # Cat 8: aria-hidden with instructional content
    aria_hidden_injection_found: bool = False
    aria_hidden_injection_count: int = 0
    aria_hidden_samples: list[str] = field(default_factory=list)

    # Summary
    patterns_found: int = 0  # active categories (0-8)
    severity: str = "clean"  # "clean" | "suspicious" | "critical"
    risk_level: str = "none"  # "none" | "low" | "medium" | "high"


# ─── Negative Signals Detection ───────────────────────────────────────────────


@dataclass
class NegativeSignalsResult:
    """Negative signals that reduce the probability of AI citation."""

    checked: bool = False

    # 1. Excessive CTA density (self-promotional)
    cta_density_high: bool = False
    cta_count: int = 0

    # 2. Popup/interstitial in the DOM
    has_popup_signals: bool = False
    popup_indicators: list[str] = field(default_factory=list)

    # 3. Thin content
    is_thin_content: bool = False  # < 300 words with complex H1

    # 4. Broken/empty internal links
    broken_links_count: int = 0
    has_broken_links: bool = False

    # 5. Keyword stuffing
    has_keyword_stuffing: bool = False
    stuffed_word: str = ""
    stuffed_density: float = 0.0

    # 6. Missing author signal
    has_author_signal: bool = False  # Person schema, rel=author, class=author

    # 7. Boilerplate ratio
    boilerplate_ratio: float = 0.0  # 0.0-1.0 (nav+footer+sidebar / total)
    boilerplate_high: bool = False  # ratio > 0.6

    # 8. Mixed signals (promise vs content)
    has_mixed_signals: bool = False
    mixed_signal_detail: str = ""

    # Summary
    signals_found: int = 0  # count of negative signals found
    severity: str = "clean"  # "clean", "low", "medium", "high"


# ─── Trust Stack Score (#273) ─────────────────────────────────────────────────


@dataclass
class TrustLayerScore:
    """Score for a single Trust Stack layer."""

    name: str  # "technical", "identity", "social", "academic", "consistency"
    label: str  # "Technical Trust"
    score: int = 0
    max_score: int = 5
    signals_found: list[str] = field(default_factory=list)
    signals_missing: list[str] = field(default_factory=list)
    details: dict[str, Any] = field(default_factory=dict)


def _make_layer(name: str, label: str) -> TrustLayerScore:
    """Factory to create a TrustLayerScore with clean defaults."""
    return TrustLayerScore(name=name, label=label)


@dataclass
class TrustStackResult:
    """5-layer trust signal aggregation (v4.5, #273). Informational — does not affect GEO score."""

    checked: bool = False
    technical: TrustLayerScore = field(default_factory=lambda: _make_layer("technical", "Technical Trust"))
    identity: TrustLayerScore = field(default_factory=lambda: _make_layer("identity", "Identity Trust"))
    social: TrustLayerScore = field(default_factory=lambda: _make_layer("social", "Social Trust"))
    academic: TrustLayerScore = field(default_factory=lambda: _make_layer("academic", "Academic Trust"))
    consistency: TrustLayerScore = field(default_factory=lambda: _make_layer("consistency", "Consistency Trust"))
    composite_score: int = 0  # 0-25
    grade: str = "F"  # A/B/C/D/F
    trust_level: str = "low"  # "low" | "medium" | "high" | "excellent"


# ─── RAG Chunk Readiness (v4.7) ──────────────────────────────────────────────


@dataclass
class RagChunkResult:
    """RAG chunking readiness analysis (#353)."""

    checked: bool = False
    total_sections: int = 0
    sections_in_range: int = 0
    avg_section_words: float = 0.0
    has_definition_opening: bool = False
    heading_as_boundary_ratio: float = 0.0
    anchor_sentences: int = 0
    chunk_readiness_score: int = 0


# ─── Embedding Proximity (v4.7) ─────────────────────────────────────────────


@dataclass
class EmbeddingProximityResult:
    """Embedding-based RAG retrieval simulation (#354)."""

    checked: bool = False
    skipped_reason: str | None = None
    model_name: str = ""
    query_scores: list[dict[str, Any]] = field(default_factory=list)
    avg_similarity: float = 0.0
    top_similarity: float = 0.0
    retrievable_chunks: int = 0
    total_chunks: int = 0


# ─── Semantic Coherence (v4.7) ───────────────────────────────────────────────


@dataclass
class PageTermExtract:
    """Terminology extracted from a single page for cross-page analysis (#253)."""

    url: str = ""
    title: str = ""
    h1: str = ""
    definitions: list[str] = field(default_factory=list)
    key_terms: list[str] = field(default_factory=list)
    language: str = ""
    hreflang_langs: list[str] = field(default_factory=list)


@dataclass
class CoherenceIssue:
    """A single cross-page coherence problem (#253)."""

    issue_type: str = ""  # conflicting_definition | duplicate_title | mixed_language
    severity: str = "low"  # high | medium | low
    description: str = ""
    pages: list[str] = field(default_factory=list)
    terms: list[str] = field(default_factory=list)


@dataclass
class SemanticCoherenceResult:
    """Aggregated cross-page semantic coherence analysis (#253)."""

    checked: bool = False
    pages_analyzed: int = 0
    issues: list[CoherenceIssue] = field(default_factory=list)
    coherence_score: int = 100
    language_consistency: float = 1.0


# ─── Content Decay Prediction (v4.7) ────────────────────────────────────────


@dataclass
class DecaySignal:
    """A single content decay signal (#383)."""

    decay_type: str = ""  # temporal | statistical | version | event | price
    text: str = ""
    estimated_stale_days: int = 0
    suggestion: str = ""


@dataclass
class ContentDecayResult:
    """Content decay prediction for a page (#383)."""

    checked: bool = False
    signals: list[DecaySignal] = field(default_factory=list)
    earliest_decay_days: int | None = None
    decay_risk: str = "low"  # low | medium | high
    evergreen_score: int = 100


# ─── Server Log Analysis (v4.7) ─────────────────────────────────────────────


@dataclass
class BotStats:
    """Statistics for a single AI bot from server logs (#227)."""

    bot_name: str = ""
    visits: int = 0
    unique_pages: int = 0
    first_seen: str = ""
    last_seen: str = ""


@dataclass
class CrawledPage:
    """A page crawled by AI bots (#227)."""

    path: str = ""
    total_visits: int = 0
    bots: list[str] = field(default_factory=list)


@dataclass
class LogAnalysisResult:
    """Server log analysis for AI crawler activity (#227)."""

    checked: bool = False
    log_file: str = ""
    total_lines: int = 0
    ai_requests: int = 0
    date_range_start: str = ""
    date_range_end: str = ""
    bots: list[BotStats] = field(default_factory=list)
    top_pages: list[CrawledPage] = field(default_factory=list)


# ─── Multi-Platform Citation Profile (v4.7) ─────────────────────────────────


@dataclass
class PlatformScore:
    """Readiness score for a specific AI platform (#228)."""

    platform: str = ""
    score: int = 0
    strengths: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)


@dataclass
class PlatformCitationResult:
    """Multi-platform citation readiness profile (#228)."""

    checked: bool = False
    platforms: list[PlatformScore] = field(default_factory=list)


# ─── Brand Sentiment Analysis (v4.7) ────────────────────────────────────────


@dataclass
class BrandSentimentResult:
    """Brand sentiment analysis from LLM responses (#378)."""

    checked: bool = False
    skipped_reason: str | None = None
    brand: str = ""
    overall_score: int = 0  # -100 (negative) to +100 (positive)
    sentiment: str = "unknown"  # positive | neutral | negative | unknown
    positive_phrases: list[str] = field(default_factory=list)
    negative_phrases: list[str] = field(default_factory=list)
    recommendation_strength: str = ""  # strongly_recommended | mentioned | neutral | warned_against
    llm_provider: str = ""
    llm_model: str = ""
    raw_response: str = ""


# ─── Citation Attribution Chain (v4.7) ───────────────────────────────────────


@dataclass
class AttributionSegment:
    """A segment of LLM response matched to source content (#375)."""

    llm_text: str = ""
    source_text: str = ""
    similarity: float = 0.0
    faithfulness: str = ""  # faithful | paraphrased | altered | hallucinated


@dataclass
class CitationAttributionResult:
    """Citation attribution chain analysis (#375)."""

    checked: bool = False
    skipped_reason: str | None = None
    query: str = ""
    segments: list[AttributionSegment] = field(default_factory=list)
    faithfulness_score: float = 0.0  # 0-1
    details_lost: list[str] = field(default_factory=list)
    details_added: list[str] = field(default_factory=list)
    llm_provider: str = ""
    llm_model: str = ""


# ─── Multi-Turn Persistence (v4.7) ──────────────────────────────────────────


@dataclass
class TurnResult:
    """Result of a single conversation turn (#376)."""

    turn: int = 0
    query: str = ""
    brand_mentioned: bool = False
    mention_count: int = 0
    response_snippet: str = ""


@dataclass
class MultiTurnResult:
    """Multi-turn conversation persistence analysis (#376)."""

    checked: bool = False
    skipped_reason: str | None = None
    brand: str = ""
    turns: list[TurnResult] = field(default_factory=list)
    persistence_score: int = 0  # 0-100
    last_mentioned_turn: int = 0
    total_turns: int = 0
    llm_provider: str = ""
    llm_model: str = ""


# ─── Cross-Platform Citation Map (v4.7) ─────────────────────────────────────


@dataclass
class CitationMapEntry:
    """A single entry in the cross-platform citation map (#356)."""

    query: str = ""
    platform: str = ""
    brand_mentioned: bool = False
    sentiment: str = ""  # positive | neutral | negative
    faithfulness: float = 0.0
    snippet: str = ""


@dataclass
class CitationMapResult:
    """Cross-platform citation map aggregation (#356)."""

    checked: bool = False
    skipped_reason: str | None = None
    brand: str = ""
    entries: list[CitationMapEntry] = field(default_factory=list)
    platforms_tested: int = 0
    platforms_citing: int = 0
    overall_visibility: float = 0.0  # 0-1


# ─── Prompt Library (v4.7) ───────────────────────────────────────────────────


@dataclass
class PromptResult:
    """Result of executing a single prompt (#379)."""

    intent: str = ""
    prompt: str = ""
    brand_mentioned: bool = False
    mention_count: int = 0
    sentiment: str = ""
    response_snippet: str = ""


@dataclass
class PromptLibraryResult:
    """Batch prompt execution results (#379)."""

    checked: bool = False
    skipped_reason: str | None = None
    brand: str = ""
    results: list[PromptResult] = field(default_factory=list)
    mention_rate: float = 0.0  # 0-1
    avg_sentiment_score: float = 0.0
    llm_provider: str = ""
    llm_model: str = ""


# ─── Context Window Optimization (v4.9) ─────────────────────────────────────


@dataclass
class ContextWindowResult:
    """Context window utilization analysis (#370). Informational — does not affect GEO score."""

    checked: bool = False
    total_words: int = 0
    total_tokens_estimate: int = 0
    front_loaded_ratio: float = 0.0  # % of key info in first 30% of content
    key_info_tokens: int = 0  # tokens containing key information
    filler_ratio: float = 0.0  # % of tokens that are boilerplate/filler
    optimal_for: list[str] = field(default_factory=list)  # ["rag_chunk", "perplexity", "chatgpt", ...]
    truncation_risk: str = "none"  # none | low | medium | high
    context_efficiency_score: int = 0  # 0-100


# ─── Instruction Following Readiness (v4.9) ─────────────────────────────────


@dataclass
class InstructionReadinessResult:
    """AI agent instruction following readiness (#371). Informational — does not affect GEO score."""

    checked: bool = False
    # Action clarity: CTAs with descriptive text
    labeled_buttons: int = 0
    unlabeled_buttons: int = 0
    action_clarity_score: int = 0  # 0-100
    # Form machine-readability
    total_inputs: int = 0
    labeled_inputs: int = 0
    typed_inputs: int = 0  # inputs with explicit type attribute
    form_readability_score: int = 0  # 0-100
    # Workflow linearity: navigation complexity
    nav_links: int = 0
    stateful_urls: bool = False  # URLs with query params or hash fragments
    # Error recovery: machine-readable error patterns
    has_aria_live: bool = False
    has_error_roles: bool = False  # role="alert" or aria-invalid
    # Summary
    readiness_score: int = 0  # 0-100
    readiness_level: str = "none"  # none | basic | ready | advanced


# ─── Vertical Market Readiness ───────────────────────────────────────────────


@dataclass
class VerticalSignal:
    """Single buyer-facing readiness signal for a vertical profile."""

    key: str = ""
    label: str = ""
    detected: bool = False
    evidence: list[str] = field(default_factory=list)


@dataclass
class VerticalAuditResult:
    """Business-facing readiness layer for local service verticals."""

    checked: bool = False
    vertical: str = "generic"
    detected_vertical: str = "generic"
    detection_confidence: float = 0.0
    market_locale: str = "en"
    trust_signals: int = 0
    conversion_signals: int = 0
    locality_signals: int = 0
    vertical_signals: int = 0
    bilingual_ready: bool = False
    business_readiness_score: int = 0
    signals: list[VerticalSignal] = field(default_factory=list)
    priority_actions: list[str] = field(default_factory=list)


# ─── Action Intelligence ──────────────────────────────────────────────────────


@dataclass
class NextAction:
    """Prioritized execution item generated from score gaps."""

    key: str = ""
    title: str = ""
    why: str = ""
    impact: str = "medium"  # low | medium | high
    effort: str = "medium"  # low | medium | high
    priority: str = "P2"  # P1 | P2 | P3
    expected_score_gain: int = 0


# ─── Marketing audit (v4.12) ─────────────────────────────────────────────────


@dataclass
class CopywritingResult:
    """Copywriting quality analysis — headline, value prop, CTAs, benefit language."""

    checked: bool = False
    # Headline (H1)
    h1_text: str = ""
    h1_is_outcome_focused: bool = False  # mentions what customer gets/achieves
    h1_is_feature_focused: bool = False  # talks about what we do/offer
    h1_is_generic: bool = False  # vague/empty ("Welcome", "Home", etc.)
    # Value proposition
    has_value_prop_in_hero: bool = False  # clear "you get X" framing above fold
    value_prop_snippet: str = ""
    # CTA copy quality
    weak_ctas: list[str] = field(default_factory=list)  # "Submit", "Learn More", etc.
    strong_ctas: list[str] = field(default_factory=list)  # "Start Free Trial", etc.
    # Benefit vs. feature language
    benefit_phrases: int = 0  # "you get", "your", outcome language
    feature_phrases: int = 0  # "we offer", "our product", "we provide"
    benefit_ratio: float = 0.0  # benefit / (benefit + feature), 0.0–1.0
    # H2 heading quality
    h2_count: int = 0
    h2_keyword_quality: str = ""   # "good" | "generic" | "ai-focused"
    h2_service_count: int = 0      # H2s containing real service/location keywords
    h2_samples: list[str] = field(default_factory=list)  # first 5 H2 texts
    # Issues and suggestions
    issues: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    copy_score: int = 0  # 0-100


@dataclass
class ImageAuditResult:
    """On-page image SEO audit."""

    checked: bool = False
    total_images: int = 0
    images_missing_alt: int = 0          # <img> with no alt attribute
    images_empty_alt: int = 0            # alt="" (decorative — ok if intentional)
    images_keyword_alt: int = 0          # alt text contains service/location keyword
    images_keyword_filename: int = 0     # filename contains service/location keyword
    images_webp: int = 0                 # .webp format
    images_missing_dimensions: int = 0  # missing width or height attribute
    images_missing_lazy: int = 0        # missing loading="lazy"
    issues: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    image_score: int = 0                 # 0-100


@dataclass
class ContentStrategyResult:
    """Content strategy signals — blog, FAQ, comparisons, pricing, lead capture."""

    checked: bool = False
    # Blog / content hub
    has_blog: bool = False
    blog_url: str = ""
    estimated_article_count: int = 0  # links to /blog/* found on homepage
    # FAQ
    has_faq_section: bool = False
    has_faq_schema: bool = False
    # Comparison / alternatives pages
    has_comparison_pages: bool = False
    comparison_urls: list[str] = field(default_factory=list)  # /vs/, /alternatives/
    # Pricing transparency
    has_pricing_page: bool = False
    has_pricing_md: bool = False  # /pricing.md for AI agents
    # Lead capture
    has_email_capture: bool = False  # newsletter, lead magnet, email input
    has_lead_magnet: bool = False  # free guide, template, tool mentioned
    # Case studies / proof
    has_case_studies: bool = False
    has_numbers_proof: bool = False  # "10,000 customers", "3× faster" etc.
    # Internal link depth
    internal_link_count: int = 0         # total same-domain links on page
    # LocalBusiness schema completeness
    has_local_business_schema: bool = False
    local_business_has_address: bool = False
    local_business_has_phone: bool = False
    local_business_has_hours: bool = False
    local_business_has_geo: bool = False
    # Industry trust / backlink signals
    has_industry_memberships: bool = False  # RGCQ / CORPIQ / APCHQ / BBB mentions
    industry_membership_names: list[str] = field(default_factory=list)
    # Issues and suggestions
    issues: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    content_score: int = 0  # 0-100


@dataclass
class MarketingAction:
    """Single prioritised marketing action."""

    key: str = ""
    title: str = ""
    why: str = ""
    skill: str = ""  # which marketingskill this maps to
    impact: str = "medium"  # low | medium | high
    effort: str = "medium"
    priority: str = "P2"  # P1 | P2 | P3
    estimated_lift: str = ""  # e.g. "+15-25% conversion"


@dataclass
class AIPresenceResult:
    """AI search presence checks — from the ai-seo, schema-markup, and programmatic-seo skills."""

    checked: bool = False
    # robots.txt — AI bot access (ai-seo skill: immediate visibility killer)
    robots_txt_fetched: bool = False
    blocked_ai_bots: list[str] = field(default_factory=list)   # bots with Disallow: /
    # Content extractability (ai-seo skill: Pillar 1 — Structure)
    has_definition_block: bool = False   # self-contained definition in first 300 words
    definition_snippet: str = ""
    # Statistics attribution (ai-seo skill: attributed stats > naked stats)
    has_attributed_stats: bool = False   # stats with "According to X" / "(Source, Year)"
    unattributed_stat_count: int = 0     # bare % numbers without a source
    # Technical presence (ai-seo skill: Pillar 3 — Discoverable)
    js_heavy: bool = False               # high script:text ratio → likely JS-rendered SPA
    # Programmatic SEO — location pages (programmatic-seo skill: Locations playbook)
    has_location_pages: bool = False
    location_page_count: int = 0
    # Entity authority (schema-markup skill: Organization sameAs + author attribution)
    has_org_sameas: bool = False         # Organization schema with sameAs links
    has_author_schema: bool = False      # Person schema with credentials / sameAs
    # Issues and suggestions
    issues: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    presence_score: int = 0  # 0-100


@dataclass
class MediaAsset:
    """Single video or audio asset found on the page."""

    url: str = ""
    media_type: str = ""     # "video" | "audio"
    format: str = ""         # "mp4" | "webm" | "mp3" | "ogg" | "unknown"
    size_bytes: int = -1     # -1 = not checked
    has_lazy_load: bool = False
    has_poster: bool = False         # video: poster= attribute
    autoplay_unmuted: bool = False   # video: autoplay without muted
    has_dimensions: bool = False     # width + height attributes present
    has_responsive_sources: bool = False  # <source media="(max-width:…)"> variants
    has_webm_source: bool = False         # WebM <source> present as fallback


@dataclass
class MediaResult:
    """Media optimization audit — video/audio assets on the page."""

    checked: bool = False
    video_count: int = 0
    audio_count: int = 0
    assets: list[MediaAsset] = field(default_factory=list)
    large_videos: int = 0               # videos > 5 MB
    large_audios: int = 0               # audio > 2 MB
    missing_lazy: int = 0               # media without lazy-load
    missing_poster: int = 0             # videos without poster frame
    autoplay_unmuted: int = 0           # autoplay without muted (bad UX + layout shift)
    non_mp4_videos: int = 0             # videos not served as mp4/webm
    missing_responsive_sources: int = 0 # videos without mobile/desktop <source media=...>
    no_webm_fallback: int = 0           # MP4-only videos with no WebM <source>
    issues: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    media_score: int = 100       # starts at 100, deductions per issue


@dataclass
class SerpCompetitor:
    """Single competitor page from SERP analysis."""

    rank: int = 0
    url: str = ""
    title: str = ""
    description: str = ""
    word_count: int = 0
    h1: str = ""
    h2_count: int = 0
    h2_texts: list[str] = field(default_factory=list)  # actual H2 text for keyword gap analysis
    has_location_pages: bool = False  # competitor has /location/ or /cities/ pattern
    has_schema: bool = False
    schema_types: list[str] = field(default_factory=list)
    has_faq: bool = False
    has_video: bool = False
    has_images: bool = False
    internal_links: int = 0
    content_snippet: str = ""  # first 200 chars of body text


@dataclass
class SerpResult:
    """SERP keyword competitor analysis."""

    checked: bool = False
    keyword: str = ""
    search_engine: str = "duckduckgo"
    competitors: list[SerpCompetitor] = field(default_factory=list)
    # Gap analysis vs audited site
    avg_competitor_word_count: int = 0
    your_word_count: int = 0
    word_count_gap: int = 0          # how many words behind top competitors
    avg_competitor_h2s: float = 0.0
    competitors_with_schema: int = 0
    competitors_with_faq: int = 0
    competitors_with_video: int = 0
    # Suggested location pages (service × city combos)
    location_page_suggestions: list[str] = field(default_factory=list)
    # Keyword gap vs first-page competitors
    keyword_gaps: list[str] = field(default_factory=list)      # topics in competitor H2s not on your page
    page1_requirements: list[str] = field(default_factory=list) # actionable "to rank page 1 you need X" list
    competitors_with_location_pages: int = 0
    # Issues and action items
    issues: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)


@dataclass
class MarketingResult:
    """Combined marketing audit result — copywriting + content strategy + AI presence."""

    checked: bool = False
    marketing_score: int = 0  # 0-100 composite
    copywriting: CopywritingResult = field(default_factory=CopywritingResult)
    content_strategy: ContentStrategyResult = field(default_factory=ContentStrategyResult)
    ai_presence: AIPresenceResult = field(default_factory=AIPresenceResult)
    image_audit: ImageAuditResult = field(default_factory=ImageAuditResult)
    media: MediaResult = field(default_factory=MediaResult)
    serp: SerpResult = field(default_factory=SerpResult)
    priority_actions: list[MarketingAction] = field(default_factory=list)


# ─── Performance audit (v4.12) ───────────────────────────────────────────────


@dataclass
class PerfIssue:
    """Single performance / load-speed issue."""

    check: str = ""  # e.g. "img_missing_dimensions"
    severity: str = "warning"  # warning | error
    element: str = ""  # short HTML snippet or URL fragment
    fix: str = ""  # one-line remediation hint


@dataclass
class PerfResult:
    """Core Web Vitals / performance audit result. Informational — does not affect GEO score."""

    checked: bool = False
    images_missing_dimensions: int = 0  # <img> without width + height
    images_missing_lazy: int = 0  # <img> without loading="lazy"
    render_blocking_scripts: int = 0  # <script> without async/defer
    render_blocking_styles: int = 0  # <link rel="stylesheet"> in <head>
    missing_font_display_swap: bool = False  # @font-face without font-display:swap
    issues: list[PerfIssue] = field(default_factory=list)
    perf_score: int = 0  # 0-100 (higher = fewer issues)


# ─── Broken link / 404 audit (v4.12) ─────────────────────────────────────────


@dataclass
class LinkIssue:
    """Single broken or redirected internal link."""

    url: str = ""
    status: int = 0  # HTTP status code (404, 500, 0 = timeout)
    anchor_text: str = ""
    source_page: str = ""  # which page contained this link


@dataclass
class LinksResult:
    """Broken link + 404 audit result. Informational — does not affect GEO score."""

    checked: bool = False
    total_internal_links: int = 0
    broken_links: list[LinkIssue] = field(default_factory=list)
    redirect_chains: list[LinkIssue] = field(default_factory=list)  # 301/302 chains
    broken_count: int = 0
    vercel_redirects_block: str = ""  # Ready-to-paste JSON for vercel.json
    # External link checking (opt-in via --check-external)
    external_broken_links: list[LinkIssue] = field(default_factory=list)
    external_broken_count: int = 0
    # Canonical-redirect conflict: canonical points to a URL that then redirects
    canonical_redirect_conflict: bool = False
    canonical_url: str = ""  # value of <link rel="canonical">
    canonical_redirects_to: str = ""  # final URL after redirect (if conflict)
    # Breadcrumb detection
    has_breadcrumbs: bool = False
    breadcrumb_type: str = ""  # "schema", "nav", "aria" or ""


# ─── Conversion readiness audit (v4.12) ──────────────────────────────────────


@dataclass
class ConversionSignal:
    """Single conversion readiness signal."""

    key: str = ""
    label: str = ""
    detected: bool = False
    evidence: str = ""  # snippet or selector that triggered detection
    fix: str = ""  # actionable one-liner if not detected


@dataclass
class ConversionResult:
    """Conversion readiness checklist. Informational — does not affect GEO score."""

    checked: bool = False
    cta_above_fold: bool = False  # primary CTA visible without scrolling
    has_contact_form: bool = False  # <form> with email/tel input
    has_phone_number: bool = False  # tel: link or phone-like text
    has_testimonials: bool = False  # review/testimonial section
    has_aggregate_rating: bool = False  # AggregateRating schema
    has_trust_badges: bool = False  # SSL, guarantee, award mentions
    cta_count: int = 0  # total CTA buttons/links
    signals: list[ConversionSignal] = field(default_factory=list)
    conversion_score: int = 0  # 0-100
    priority_fixes: list[str] = field(default_factory=list)  # top 3 copy suggestions
    # form-cro extensions (v4.13)
    max_form_fields: int = 0  # highest field count across all forms
    has_strong_submit_copy: bool = False  # submit button uses action-oriented copy
    has_privacy_near_form: bool = False  # privacy/no-spam text near form
    has_social_auth: bool = False  # Google/Apple/Microsoft OAuth buttons present
    has_mobile_viewport: bool = False  # <meta name="viewport"> present


# ─── Analytics / tracking audit (v4.13) ─────────────────────────────────────


@dataclass
class TrackingSignal:
    """Single analytics/tracking tool detection."""

    key: str = ""
    label: str = ""
    detected: bool = False
    evidence: str = ""  # script src snippet or trigger
    fix: str = ""


@dataclass
class TrackingResult:
    """Analytics and conversion tracking audit. Informational — does not affect GEO score."""

    checked: bool = False
    has_analytics: bool = False  # any analytics tool detected
    has_conversion_tracking: bool = False  # conversion pixel or goal tracking
    has_ga4: bool = False  # Google Analytics 4
    has_gtm: bool = False  # Google Tag Manager
    has_meta_pixel: bool = False  # Meta/Facebook Pixel
    has_other_analytics: bool = False  # Plausible, Fathom, Matomo, Segment, etc.
    has_heatmap: bool = False  # Hotjar, Microsoft Clarity, etc.
    signals: list[TrackingSignal] = field(default_factory=list)
    tracking_score: int = 0  # 0-100
    priority_fixes: list[str] = field(default_factory=list)


# ─── Indexability conflict audit ─────────────────────────────────────────────


@dataclass
class IndexabilityResult:
    """Three-layer indexability conflict check. Informational — generates critical recommendations."""

    checked: bool = False
    # Layer 1: robots.txt (already in RobotsResult — cross-reference only)
    # Layer 2: <meta name="robots"> page-level directive
    meta_robots_content: str = ""  # raw content string e.g. "noindex, nosnippet"
    meta_noindex: bool = False
    meta_nosnippet: bool = False  # blocks AI Overviews and AI Mode (Google-documented)
    meta_max_snippet: int = -1  # -1 = unrestricted; 0 = no snippet
    # Layer 3: X-Robots-Tag response header
    x_robots_content: str = ""
    x_robots_noindex: bool = False
    x_robots_nosnippet: bool = False
    x_robots_max_snippet: int = -1
    # Conflict detection
    has_nosnippet: bool = False  # either meta or header
    has_noindex: bool = False  # either meta or header
    # robots.txt allows but page-level says noindex — silent suppression
    robots_meta_conflict: bool = False
    conflict_detail: str = ""


# ─── Freshness audit ──────────────────────────────────────────────────────────


@dataclass
class FreshnessResult:
    """Freshness signals audit. Informational — supplements signals.has_freshness."""

    checked: bool = False
    # Visible date in HTML body (human-readable, near top of page)
    visible_date_text: str = ""  # e.g. "January 15, 2025"
    visible_date_near_top: bool = False  # within first 500 words
    # HTTP Last-Modified header
    last_modified_header: str = ""
    has_last_modified: bool = False
    # Schema dateModified (already in SchemaResult — cross-reference for agreement)
    schema_date: str = ""
    # Agreement: schema date and visible date agree (within 7 days)
    date_agreement: bool = False
    date_conflict: bool = False  # schema and visible dates contradict each other
    conflict_detail: str = ""
    # datetime attributes on <time> elements
    has_time_element: bool = False
    time_datetime: str = ""


# ─── IndexNow ────────────────────────────────────────────────────────────────


@dataclass
class IndexNowResult:
    """IndexNow protocol readiness check."""

    checked: bool = False
    is_configured: bool = False
    has_meta_tag: bool = False        # <meta name="indexnow-key">
    has_link_element: bool = False    # <link rel="indexnow">
    key_value: str = ""               # raw key string found
    key_looks_valid: bool = False     # matches 32–128 hex chars
    key_url: str = ""                 # expected key file URL
    recommendations: list[str] = field(default_factory=list)


# ─── AEO (Answer Engine Optimization) ────────────────────────────────────────


@dataclass
class AEOResult:
    """Answer Engine Optimization audit: Featured Snippets, PAA, Knowledge Panel."""

    checked: bool = False

    # Featured Snippet
    has_paragraph_snippet_candidate: bool = False
    snippet_candidate_word_count: int = 0
    has_list_snippet_candidate: bool = False
    list_snippet_item_count: int = 0
    has_table_snippet_candidate: bool = False
    featured_snippet_score: int = 0   # 0–3

    # People Also Ask
    question_heading_count: int = 0
    has_question_headings: bool = False
    faq_schema_item_count: int = 0
    has_faq_schema: bool = False
    paa_question_types_covered: list[str] = field(default_factory=list)
    paa_score: int = 0                # 0–3

    # Knowledge Panel
    kg_same_as_count: int = 0
    kg_authoritative_same_as: int = 0
    has_wikidata_link: bool = False
    has_wikipedia_link: bool = False
    has_org_schema: bool = False
    has_nap_consistency: bool = False
    has_founder_entity: bool = False
    knowledge_panel_score: int = 0    # 0–4

    recommendations: list[str] = field(default_factory=list)


# ─── SXO (Search Experience Optimization) ────────────────────────────────────


@dataclass
class SXOResult:
    """Search Experience Optimization: intent-content alignment audit."""

    checked: bool = False
    page_url: str = ""

    # Detected signals
    url_intent_signals: list[str] = field(default_factory=list)      # e.g. ["transactional"]
    content_intent_signals: list[str] = field(default_factory=list)  # e.g. ["informational"]
    cta_count: int = 0
    word_count: int = 0

    # Alignment result
    intent_aligned: bool = True
    matched_intent: str = ""          # dominant intent when aligned
    mismatch_type: str = ""           # e.g. "transactional_url_informational_content"
    mismatch_detail: str = ""         # human-readable explanation

    # Dimension checks
    informational_depth_ok: bool = True

    sxo_score: int = 0               # 0–3
    recommendations: list[str] = field(default_factory=list)


# ─── Full audit ──────────────────────────────────────────────────────────────


@dataclass
class AuditResult:
    url: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    score: int = 0
    band: str = "critical"
    robots: RobotsResult = field(default_factory=RobotsResult)
    llms: LlmsTxtResult = field(default_factory=LlmsTxtResult)
    schema: SchemaResult = field(default_factory=SchemaResult)
    meta: MetaResult = field(default_factory=MetaResult)
    content: ContentResult = field(default_factory=ContentResult)
    recommendations: list[str] = field(default_factory=list)
    http_status: int = 0
    page_size: int = 0
    # Citability: score 0-100 based on the 9 Princeton KDD 2024 methods
    citability: CitabilityResult = field(default_factory=CitabilityResult)
    # Fix #104: CheckRegistry plugin results (do not affect the base score)
    extra_checks: dict[str, Any] = field(default_factory=dict)
    # v4.0: technical signals (lang, RSS, freshness)
    signals: SignalsResult = field(default_factory=SignalsResult)
    # v4.1: AI discovery endpoints (geo-checklist.dev)
    ai_discovery: AiDiscoveryResult = field(default_factory=AiDiscoveryResult)
    # v4.0: score breakdown per category
    score_breakdown: dict[str, int] = field(default_factory=dict)
    # v4.0: connection error message (None = success)
    error: str | None = None
    # v4.2: CDN AI Crawler check (#225)
    cdn_check: CdnAiCrawlerResult = field(default_factory=CdnAiCrawlerResult)
    # v4.2: JS Rendering check (#226)
    js_rendering: JsRenderingResult = field(default_factory=JsRenderingResult)
    # v4.3: Brand & Entity signals
    brand_entity: BrandEntityResult = field(default_factory=BrandEntityResult)
    # v4.3: WebMCP Readiness check (#233)
    webmcp: WebMcpResult = field(default_factory=WebMcpResult)
    # v4.3: Negative Signals detection
    negative_signals: NegativeSignalsResult = field(default_factory=NegativeSignalsResult)
    # v4.4: Prompt Injection Pattern Detection (#276)
    prompt_injection: PromptInjectionResult = field(default_factory=PromptInjectionResult)
    # v4.5: Trust Stack Score — informational, does not affect GEO score (#273)
    trust_stack: TrustStackResult = field(default_factory=TrustStackResult)
    # v4.7: audit wall-clock duration in milliseconds (#290)
    audit_duration_ms: int | None = None
    # v4.7: RAG chunk readiness (#353)
    rag_chunk: RagChunkResult = field(default_factory=RagChunkResult)
    # v4.7: Embedding proximity score (#354)
    embedding_proximity: EmbeddingProximityResult = field(default_factory=EmbeddingProximityResult)
    # v4.7: Content decay prediction (#383)
    content_decay: ContentDecayResult = field(default_factory=ContentDecayResult)
    # v4.7: Multi-platform citation profile (#228)
    platform_citation: PlatformCitationResult = field(default_factory=PlatformCitationResult)
    # v4.7: Brand sentiment analysis (#378) — opt-in, requires LLM API key
    brand_sentiment: BrandSentimentResult = field(default_factory=BrandSentimentResult)
    # v4.9: Context window optimization (#370)
    context_window: ContextWindowResult = field(default_factory=ContextWindowResult)
    # v4.9: Instruction following readiness (#371)
    instruction_readiness: InstructionReadinessResult = field(default_factory=InstructionReadinessResult)
    # v4.10: buyer-facing vertical profile for local service businesses
    vertical_profile: VerticalAuditResult = field(default_factory=VerticalAuditResult)
    # v4.11: prioritized execution roadmap
    next_actions: list[NextAction] = field(default_factory=list)
    # v4.12: performance / Core Web Vitals signals — informational
    perf: PerfResult = field(default_factory=PerfResult)
    # v4.12: broken link + 404 detection — informational
    links: LinksResult = field(default_factory=LinksResult)
    # v4.12: conversion readiness checklist — informational
    conversion: ConversionResult = field(default_factory=ConversionResult)
    # v4.13: analytics / tracking presence — informational
    tracking: TrackingResult = field(default_factory=TrackingResult)
    # v4.14: indexability conflict detection — informational
    indexability: IndexabilityResult = field(default_factory=IndexabilityResult)
    # v4.14: freshness signals — informational
    freshness: FreshnessResult = field(default_factory=FreshnessResult)
    # v4.10: IndexNow protocol readiness
    indexnow: IndexNowResult = field(default_factory=IndexNowResult)
    # v4.10: Answer Engine Optimization (Featured Snippet / PAA / Knowledge Panel)
    aeo: AEOResult = field(default_factory=AEOResult)
    # v4.10: Search Experience Optimization (intent-content alignment)
    sxo: SXOResult = field(default_factory=SXOResult)


# ─── Batch audit ─────────────────────────────────────────────────────────────


@dataclass
class BatchAuditPageResult:
    """Sintesi di un audit pagina all'interno di un audit batch da sitemap."""

    url: str
    score: int = 0
    band: str = "critical"
    http_status: int = 0
    error: str | None = None
    score_breakdown: dict[str, int] = field(default_factory=dict)
    recommendations_count: int = 0


@dataclass
class BatchAuditResult:
    """Risultato aggregato di un audit batch eseguito su una sitemap."""

    sitemap_url: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    discovered_urls: int = 0
    audited_urls: int = 0
    successful_urls: int = 0
    failed_urls: int = 0
    average_score: float = 0.0
    average_band: str = "critical"
    band_counts: dict[str, int] = field(default_factory=dict)
    average_score_breakdown: dict[str, float] = field(default_factory=dict)
    pages: list[BatchAuditPageResult] = field(default_factory=list)
    top_pages: list[BatchAuditPageResult] = field(default_factory=list)
    worst_pages: list[BatchAuditPageResult] = field(default_factory=list)


# ─── Audit diff ──────────────────────────────────────────────────────────────


@dataclass
class CategoryDelta:
    """Delta di punteggio per una singola categoria GEO tra due audit."""

    category: str
    label: str
    before_score: int = 0
    after_score: int = 0
    delta: int = 0
    max_score: int = 0


@dataclass
class AuditDiffResult:
    """Confronto A/B tra due audit GEO della stessa o di due diverse pagine."""

    before_url: str
    after_url: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    before_score: int = 0
    after_score: int = 0
    score_delta: int = 0
    before_band: str = "critical"
    after_band: str = "critical"
    before_http_status: int = 0
    after_http_status: int = 0
    before_error: str | None = None
    after_error: str | None = None
    before_recommendations_count: int = 0
    after_recommendations_count: int = 0
    recommendations_delta: int = 0
    category_deltas: list[CategoryDelta] = field(default_factory=list)
    improved_categories: list[CategoryDelta] = field(default_factory=list)
    regressed_categories: list[CategoryDelta] = field(default_factory=list)
    unchanged_categories: list[CategoryDelta] = field(default_factory=list)


# ─── Gap analysis ────────────────────────────────────────────────────────────


@dataclass
class GapAction:
    """Azione consigliata per colmare un gap GEO rispetto a un competitor."""

    category: str
    title: str
    rationale: str
    impact_points: int = 0
    priority: str = "medium"
    command: str = ""


@dataclass
class GapAnalysisResult:
    """Gap analysis interpretativa tra due siti GEO."""

    weaker_url: str
    stronger_url: str
    weaker_score: int = 0
    stronger_score: int = 0
    score_gap: int = 0
    weaker_band: str = "critical"
    stronger_band: str = "critical"
    category_deltas: list[CategoryDelta] = field(default_factory=list)
    action_plan: list[GapAction] = field(default_factory=list)
    strengths: list[CategoryDelta] = field(default_factory=list)


# ─── Factual accuracy ────────────────────────────────────────────────────────


@dataclass
class FactualAccuracyResult:
    """Audit euristico di claims, fonti e incoerenze fattuali."""

    checked: bool = False
    claims_found: int = 0
    claims_sourced: int = 0
    claims_unsourced: int = 0
    unsourced_claims: list[str] = field(default_factory=list)
    unverifiable_claims: list[str] = field(default_factory=list)
    inconsistencies: list[str] = field(default_factory=list)
    broken_source_links: list[str] = field(default_factory=list)
    source_links_checked: int = 0
    severity: str = "clean"


# ─── Passive monitor ────────────────────────────────────────────────────────


@dataclass
class MonitorSignal:
    """Segnale sintetico per il monitoraggio passivo della visibilita' AI."""

    key: str
    label: str
    score: int = 0
    max_score: int = 0
    status: str = "missing"
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class MonitorResult:
    """Snapshot di visibilita' AI in modalita' passiva per un dominio."""

    domain: str
    url: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    mode: str = "passive"
    direct_mentions_checked: bool = False
    visibility_score: int = 0
    band: str = "low"
    total_snapshots: int = 0
    score_delta: int | None = None
    latest_geo_score: int | None = None
    latest_geo_band: str | None = None
    signals: list[MonitorSignal] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)


# ─── Answer snapshots ───────────────────────────────────────────────────────


@dataclass
class AnswerCitation:
    """Citazione estratta o registrata per uno snapshot di risposta AI."""

    url: str
    position: int = 0
    domain: str = ""


@dataclass
class AnswerSnapshot:
    """Snapshot completo di una risposta AI archiviata localmente."""

    snapshot_id: int = 0
    query: str = ""
    prompt: str = ""
    model: str = ""
    provider: str = ""
    answer_text: str = ""
    recorded_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    citations: list[AnswerCitation] = field(default_factory=list)


@dataclass
class AnswerSnapshotArchive:
    """Risultato query sull'archivio locale di snapshot AI."""

    query: str = ""
    date_from: str | None = None
    date_to: str | None = None
    total_snapshots: int = 0
    entries: list[AnswerSnapshot] = field(default_factory=list)


# ─── Citation quality ───────────────────────────────────────────────────────


@dataclass
class CitationQualityResult:
    """Valutazione qualitativa di una singola citazione dentro una risposta AI."""

    url: str
    domain: str = ""
    position: int = 0
    tier: int = 5
    tier_label: str = "mentioned"
    cue: str = ""
    position_score: int = 0
    overall_score: int = 0
    context_snippet: str = ""


@dataclass
class CitationQualityReport:
    """Analisi qualitativa delle citazioni per uno snapshot archiviato."""

    snapshot_id: int = 0
    query: str = ""
    model: str = ""
    provider: str = ""
    recorded_at: str = ""
    target_domain: str = ""
    total_citations: int = 0
    analyzed_citations: int = 0
    entries: list[CitationQualityResult] = field(default_factory=list)


# ─── History / tracking ─────────────────────────────────────────────────────


@dataclass
class HistoryEntry:
    """Snapshot storico di un audit GEO salvato localmente."""

    url: str
    timestamp: str
    score: int = 0
    band: str = "critical"
    http_status: int = 0
    recommendations_count: int = 0
    score_breakdown: dict[str, int] = field(default_factory=dict)
    delta: int | None = None


@dataclass
class HistoryResult:
    """Serie temporale degli audit GEO salvati per una URL."""

    url: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    retention_days: int = 0
    total_snapshots: int = 0
    latest_score: int | None = None
    latest_band: str | None = None
    previous_score: int | None = None
    score_delta: int | None = None
    regression_detected: bool = False
    best_score: int | None = None
    worst_score: int | None = None
    entries: list[HistoryEntry] = field(default_factory=list)


# ─── Schema analysis ─────────────────────────────────────────────────────────


@dataclass
class SchemaAnalysis:
    found_schemas: list[dict] = field(default_factory=list)
    found_types: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)
    extracted_faqs: list[dict[str, str]] = field(default_factory=list)
    duplicates: dict[str, int] = field(default_factory=dict)
    has_head: bool = False
    total_scripts: int = 0


# ─── llms.txt generation ─────────────────────────────────────────────────────


@dataclass
class SitemapUrl:
    url: str
    lastmod: str | None = None
    priority: float = 0.5
    title: str | None = None


# ─── Fix plan ───────────────────────────────────────────────────────────────


@dataclass
class FixItem:
    """Single fix generated by geo fix."""

    category: str  # "robots", "llms", "schema", "meta"
    description: str  # "Adds 5 missing AI bots to robots.txt"
    content: str  # Generated content (file text or HTML tag)
    file_name: str  # "robots.txt", "llms.txt", "schema-website.json"
    action: str  # "create", "append", "snippet"


@dataclass
class FixPlan:
    """Complete fix plan generated by geo fix."""

    url: str
    score_before: int = 0
    score_estimated_after: int = 0
    fixes: list[FixItem] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)


# ─── Content workflow (keyword + E-E-A-T + entity) ─────────────────────────


@dataclass
class KeywordDensityItem:
    """Singolo termine/frase con frequenza e densita' percentuale."""

    keyword: str
    count: int = 0
    density_pct: float = 0.0


@dataclass
class ContentWorkflowResult:
    """Audit contenutistico operativo ispirato ai workflow SEO agentici."""

    source: str = ""
    analyzed_words: int = 0
    top_terms: list[KeywordDensityItem] = field(default_factory=list)
    target_keywords: list[KeywordDensityItem] = field(default_factory=list)
    keyword_stuffing: MethodScore = field(
        default_factory=lambda: MethodScore(name="keyword_stuffing", label="Keyword Stuffing")
    )
    eeat_signals: MethodScore = field(default_factory=lambda: MethodScore(name="eeat_signals", label="E-E-A-T Signals"))
    anchor_text_quality: MethodScore = field(
        default_factory=lambda: MethodScore(name="anchor_text_quality", label="Anchor Text Quality")
    )
    entity_resolution: MethodScore = field(
        default_factory=lambda: MethodScore(name="entity_resolution", label="Entity Resolution")
    )
    kg_density: MethodScore = field(default_factory=lambda: MethodScore(name="kg_density", label="Knowledge Graph Density"))
    recommendations: list[str] = field(default_factory=list)
    error: str = ""
