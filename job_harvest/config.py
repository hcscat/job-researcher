from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


DEFAULT_SITE_KEYS = [
    "saramin",
    "jobkorea",
    "linkedin",
    "wanted",
    "jumpit",
    "remember",
    "jobplanet",
    "rocketpunch",
    "blind",
]
DEFAULT_EXTRA_TERMS = ["채용", "공고"]
DEFAULT_IT_CRAWL_TERMS = [
    "개발",
    "백엔드",
    "프론트엔드",
    "풀스택",
    "데이터 엔지니어",
    "데이터 사이언티스트",
    "머신러닝",
    "AI 엔지니어",
    "플랫폼 엔지니어",
    "QA",
    "보안",
    "iOS",
    "Android",
    "frontend",
    "backend",
    "fullstack",
    "software engineer",
    "data engineer",
    "data scientist",
    "machine learning",
    "devops",
    "platform engineer",
    "security engineer",
]
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
)

ADVANCED_FILTER_FIELDS = (
    "industries",
    "salary_ranges",
    "company_types",
    "company_sizes",
    "position_levels",
    "majors",
    "certifications",
    "preferred_conditions",
    "welfare",
    "skills",
    "tags",
    "workplace_types",
    "date_posted",
    "deadline",
    "easy_apply",
    "applicant_signals",
    "network_signals",
    "leader_positions",
    "headhunting",
    "theme_tags",
)

CORE_FILTER_FIELDS = (
    "roles",
    "keywords",
    "exclude_keywords",
    "locations",
    "companies",
    "experience_levels",
    "education_levels",
    "employment_types",
    "required_terms",
)

CRITERIA_FILTER_FIELDS = CORE_FILTER_FIELDS + ADVANCED_FILTER_FIELDS
PASSIVE_FILTER_FIELDS = {
    "date_posted",
    "deadline",
    "easy_apply",
    "applicant_signals",
    "network_signals",
    "leader_positions",
    "headhunting",
}
STRICT_MATCHABLE_FIELDS = tuple(
    field_name
    for field_name in CRITERIA_FILTER_FIELDS
    if field_name not in {"exclude_keywords", "required_terms", *PASSIVE_FILTER_FIELDS}
)


@dataclass
class SearchConfig:
    sites: list[str] = field(default_factory=lambda: list(DEFAULT_SITE_KEYS))
    queries: list[str] = field(default_factory=list)
    crawl_strategy: str = "broad_it_scan"
    crawl_terms: list[str] = field(default_factory=lambda: list(DEFAULT_IT_CRAWL_TERMS))
    listing_page_limit: int = 0
    max_results_per_site: int = 8
    request_timeout_seconds: int = 20
    fetch_details: bool = True
    store_html: bool = False
    detail_refetch_hours: int = 24
    concurrency: int = 4
    pause_between_searches_seconds: float = 1.0
    ai_enrichment_enabled: bool = False
    ai_provider: str = "heuristic"
    ai_model: str = ""
    user_agent: str = DEFAULT_USER_AGENT
    browser_enabled: bool = True
    browser_headless: bool = True
    browser_timeout_seconds: int = 60


@dataclass
class CriteriaConfig:
    roles: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    exclude_keywords: list[str] = field(default_factory=list)
    locations: list[str] = field(default_factory=list)
    companies: list[str] = field(default_factory=list)
    experience_levels: list[str] = field(default_factory=list)
    education_levels: list[str] = field(default_factory=list)
    employment_types: list[str] = field(default_factory=list)
    required_terms: list[str] = field(default_factory=list)
    industries: list[str] = field(default_factory=list)
    salary_ranges: list[str] = field(default_factory=list)
    company_types: list[str] = field(default_factory=list)
    company_sizes: list[str] = field(default_factory=list)
    position_levels: list[str] = field(default_factory=list)
    majors: list[str] = field(default_factory=list)
    certifications: list[str] = field(default_factory=list)
    preferred_conditions: list[str] = field(default_factory=list)
    welfare: list[str] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    workplace_types: list[str] = field(default_factory=list)
    date_posted: list[str] = field(default_factory=list)
    deadline: list[str] = field(default_factory=list)
    easy_apply: list[str] = field(default_factory=list)
    applicant_signals: list[str] = field(default_factory=list)
    network_signals: list[str] = field(default_factory=list)
    leader_positions: list[str] = field(default_factory=list)
    headhunting: list[str] = field(default_factory=list)
    theme_tags: list[str] = field(default_factory=list)
    extra_terms: list[str] = field(default_factory=lambda: list(DEFAULT_EXTRA_TERMS))
    strict_match_groups: list[str] = field(default_factory=list)


@dataclass
class ScheduleConfig:
    enabled: bool = False
    timezone: str = "Asia/Seoul"
    mode: str = "fixed_times"
    times: list[str] = field(default_factory=lambda: ["09:00"])
    interval_hours: int = 4
    run_on_start: bool = True
    max_runs: int | None = None


@dataclass
class PreprocessingConfig:
    enabled: bool = True
    dedupe_strategy: str = "normalized_url"
    min_text_chars: int = 80
    normalize_whitespace: bool = True
    language_hints: list[str] = field(default_factory=lambda: ["ko", "en"])


@dataclass
class AIConfig:
    auth_mode: str = "none"
    api_key_env: str = "OPENAI_API_KEY"
    oauth_profile: str = ""
    external_command: str = ""
    config: dict[str, Any] = field(default_factory=dict)


@dataclass
class IntegrationConfig:
    harness_config: dict[str, Any] = field(default_factory=dict)
    mcp_servers: dict[str, Any] = field(default_factory=dict)
    skills_config: dict[str, Any] = field(default_factory=dict)
    messaging_config: dict[str, Any] = field(default_factory=dict)
    contact_email_enabled: bool = False
    contact_email_from: str = ""
    contact_default_recipients: list[str] = field(default_factory=list)
    contact_message_template: str = (
        "Hello,\n\n"
        "I am interested in {title} at {company}.\n\n"
        "Posting: {url}\n"
    )


@dataclass
class AppConfig:
    output_dir: Path
    search: SearchConfig = field(default_factory=SearchConfig)
    criteria: CriteriaConfig = field(default_factory=CriteriaConfig)
    schedule: ScheduleConfig = field(default_factory=ScheduleConfig)
    preprocessing: PreprocessingConfig = field(default_factory=PreprocessingConfig)
    ai: AIConfig = field(default_factory=AIConfig)
    integrations: IntegrationConfig = field(default_factory=IntegrationConfig)
    config_source: str = "runtime"


def _ensure_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    raise TypeError(f"Expected list, got {type(value).__name__}")


def _ensure_dict(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return {str(key): item for key, item in value.items()}
    raise TypeError(f"Expected object, got {type(value).__name__}")


def _build_search_config(raw: dict[str, Any]) -> SearchConfig:
    crawl_strategy = str(raw.get("crawl_strategy", "broad_it_scan")).strip() or "broad_it_scan"
    if crawl_strategy not in {"broad_it_scan", "query_search"}:
        raise ValueError("search.crawl_strategy must be 'broad_it_scan' or 'query_search'")

    ai_provider = str(raw.get("ai_provider", "heuristic")).strip() or "heuristic"
    if ai_provider not in {"heuristic", "openai", "external_command"}:
        raise ValueError("search.ai_provider must be 'heuristic', 'openai', or 'external_command'")

    return SearchConfig(
        sites=_ensure_list(raw.get("sites")) or list(DEFAULT_SITE_KEYS),
        queries=_ensure_list(raw.get("queries")),
        crawl_strategy=crawl_strategy,
        crawl_terms=_ensure_list(raw.get("crawl_terms")) or list(DEFAULT_IT_CRAWL_TERMS),
        listing_page_limit=max(0, int(raw.get("listing_page_limit", 0))),
        max_results_per_site=max(1, int(raw.get("max_results_per_site", 8))),
        request_timeout_seconds=max(5, int(raw.get("request_timeout_seconds", 20))),
        fetch_details=bool(raw.get("fetch_details", True)),
        store_html=bool(raw.get("store_html", False)),
        detail_refetch_hours=max(1, int(raw.get("detail_refetch_hours", 24))),
        concurrency=max(1, int(raw.get("concurrency", 4))),
        pause_between_searches_seconds=max(
            0.0, float(raw.get("pause_between_searches_seconds", 1.0))
        ),
        ai_enrichment_enabled=bool(raw.get("ai_enrichment_enabled", False)),
        ai_provider=ai_provider,
        ai_model=str(raw.get("ai_model", "")).strip(),
        user_agent=str(raw.get("user_agent", DEFAULT_USER_AGENT)).strip() or DEFAULT_USER_AGENT,
        browser_enabled=bool(raw.get("browser_enabled", True)),
        browser_headless=bool(raw.get("browser_headless", True)),
        browser_timeout_seconds=max(10, int(raw.get("browser_timeout_seconds", 60))),
    )


def _build_criteria_config(raw: dict[str, Any]) -> CriteriaConfig:
    return CriteriaConfig(
        roles=_ensure_list(raw.get("roles")),
        keywords=_ensure_list(raw.get("keywords")),
        exclude_keywords=_ensure_list(raw.get("exclude_keywords")),
        locations=_ensure_list(raw.get("locations")),
        companies=_ensure_list(raw.get("companies")),
        experience_levels=_ensure_list(raw.get("experience_levels")),
        education_levels=_ensure_list(raw.get("education_levels")),
        employment_types=_ensure_list(raw.get("employment_types")),
        required_terms=_ensure_list(raw.get("required_terms")),
        industries=_ensure_list(raw.get("industries")),
        salary_ranges=_ensure_list(raw.get("salary_ranges")),
        company_types=_ensure_list(raw.get("company_types")),
        company_sizes=_ensure_list(raw.get("company_sizes")),
        position_levels=_ensure_list(raw.get("position_levels")),
        majors=_ensure_list(raw.get("majors")),
        certifications=_ensure_list(raw.get("certifications")),
        preferred_conditions=_ensure_list(raw.get("preferred_conditions")),
        welfare=_ensure_list(raw.get("welfare")),
        skills=_ensure_list(raw.get("skills")),
        tags=_ensure_list(raw.get("tags")),
        workplace_types=_ensure_list(raw.get("workplace_types")),
        date_posted=_ensure_list(raw.get("date_posted")),
        deadline=_ensure_list(raw.get("deadline")),
        easy_apply=_ensure_list(raw.get("easy_apply")),
        applicant_signals=_ensure_list(raw.get("applicant_signals")),
        network_signals=_ensure_list(raw.get("network_signals")),
        leader_positions=_ensure_list(raw.get("leader_positions")),
        headhunting=_ensure_list(raw.get("headhunting")),
        theme_tags=_ensure_list(raw.get("theme_tags")),
        extra_terms=_ensure_list(raw.get("extra_terms")) or list(DEFAULT_EXTRA_TERMS),
        strict_match_groups=_ensure_list(raw.get("strict_match_groups")),
    )


def _build_schedule_config(raw: dict[str, Any]) -> ScheduleConfig:
    interval_hours = raw.get("interval_hours")
    if interval_hours in (None, "") and raw.get("interval_minutes") not in (None, ""):
        interval_hours = max(1, int(raw["interval_minutes"]) // 60)

    schedule = ScheduleConfig(
        enabled=bool(raw.get("enabled", False)),
        timezone=str(raw.get("timezone", "Asia/Seoul")).strip() or "Asia/Seoul",
        mode=str(raw.get("mode", "fixed_times")).strip() or "fixed_times",
        times=_ensure_list(raw.get("times")) or ["09:00"],
        interval_hours=max(1, int(interval_hours or 4)),
        run_on_start=bool(raw.get("run_on_start", True)),
        max_runs=int(raw["max_runs"]) if raw.get("max_runs") not in (None, "") else None,
    )
    if schedule.mode not in {"fixed_times", "interval_hours"}:
        raise ValueError("schedule.mode must be 'fixed_times' or 'interval_hours'")
    return schedule


def _build_preprocessing_config(raw: dict[str, Any]) -> PreprocessingConfig:
    dedupe_strategy = str(raw.get("dedupe_strategy", "normalized_url")).strip() or "normalized_url"
    if dedupe_strategy not in {"normalized_url", "site_and_title", "company_title_location"}:
        raise ValueError(
            "preprocessing.dedupe_strategy must be 'normalized_url', "
            "'site_and_title', or 'company_title_location'"
        )
    return PreprocessingConfig(
        enabled=bool(raw.get("enabled", True)),
        dedupe_strategy=dedupe_strategy,
        min_text_chars=max(0, int(raw.get("min_text_chars", 80))),
        normalize_whitespace=bool(raw.get("normalize_whitespace", True)),
        language_hints=_ensure_list(raw.get("language_hints")) or ["ko", "en"],
    )


def _build_ai_config(raw: dict[str, Any]) -> AIConfig:
    auth_mode = str(raw.get("auth_mode", "none")).strip() or "none"
    if auth_mode not in {"none", "api_key_env", "oauth_cli", "external_command"}:
        raise ValueError(
            "ai.auth_mode must be 'none', 'api_key_env', 'oauth_cli', or 'external_command'"
        )
    return AIConfig(
        auth_mode=auth_mode,
        api_key_env=str(raw.get("api_key_env", "OPENAI_API_KEY")).strip() or "OPENAI_API_KEY",
        oauth_profile=str(raw.get("oauth_profile", "")).strip(),
        external_command=str(raw.get("external_command", "")).strip(),
        config=_ensure_dict(raw.get("config")),
    )


def _build_integration_config(raw: dict[str, Any]) -> IntegrationConfig:
    return IntegrationConfig(
        harness_config=_ensure_dict(raw.get("harness_config")),
        mcp_servers=_ensure_dict(raw.get("mcp_servers")),
        skills_config=_ensure_dict(raw.get("skills_config")),
        messaging_config=_ensure_dict(raw.get("messaging_config")),
        contact_email_enabled=bool(raw.get("contact_email_enabled", False)),
        contact_email_from=str(raw.get("contact_email_from", "")).strip(),
        contact_default_recipients=_ensure_list(raw.get("contact_default_recipients")),
        contact_message_template=str(
            raw.get("contact_message_template", IntegrationConfig().contact_message_template)
        ),
    )


def build_config(
    raw: dict[str, Any] | None,
    *,
    base_dir: str | Path | None = None,
    source: str = "runtime",
) -> AppConfig:
    payload = raw or {}
    root_dir = Path(base_dir or ".").resolve()
    output_dir = payload.get("output_dir") or "./data/exports"
    search_raw = payload.get("search", {})
    criteria_raw = payload.get("criteria", {})
    schedule_raw = payload.get("schedule", {})
    preprocessing_raw = payload.get("preprocessing", {})
    ai_raw = payload.get("ai", {})
    integrations_raw = payload.get("integrations", {})
    return AppConfig(
        output_dir=(root_dir / str(output_dir)).resolve(),
        search=_build_search_config(search_raw),
        criteria=_build_criteria_config(criteria_raw),
        schedule=_build_schedule_config(schedule_raw),
        preprocessing=_build_preprocessing_config(preprocessing_raw),
        ai=_build_ai_config(ai_raw),
        integrations=_build_integration_config(integrations_raw),
        config_source=source,
    )


def load_config(path: str | Path) -> AppConfig:
    config_path = Path(path).expanduser().resolve()
    with config_path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}
    return build_config(raw, base_dir=config_path.parent, source=f"file:{config_path}")


def config_to_dict(config: AppConfig) -> dict[str, Any]:
    return {
        "output_dir": str(config.output_dir),
        "search": {
            "sites": list(config.search.sites),
            "queries": list(config.search.queries),
            "crawl_strategy": config.search.crawl_strategy,
            "crawl_terms": list(config.search.crawl_terms),
            "listing_page_limit": config.search.listing_page_limit,
            "max_results_per_site": config.search.max_results_per_site,
            "request_timeout_seconds": config.search.request_timeout_seconds,
            "fetch_details": config.search.fetch_details,
            "store_html": config.search.store_html,
            "detail_refetch_hours": config.search.detail_refetch_hours,
            "concurrency": config.search.concurrency,
            "pause_between_searches_seconds": config.search.pause_between_searches_seconds,
            "ai_enrichment_enabled": config.search.ai_enrichment_enabled,
            "ai_provider": config.search.ai_provider,
            "ai_model": config.search.ai_model,
            "user_agent": config.search.user_agent,
            "browser_enabled": config.search.browser_enabled,
            "browser_headless": config.search.browser_headless,
            "browser_timeout_seconds": config.search.browser_timeout_seconds,
        },
        "criteria": {
            "roles": list(config.criteria.roles),
            "keywords": list(config.criteria.keywords),
            "exclude_keywords": list(config.criteria.exclude_keywords),
            "locations": list(config.criteria.locations),
            "companies": list(config.criteria.companies),
            "experience_levels": list(config.criteria.experience_levels),
            "education_levels": list(config.criteria.education_levels),
            "employment_types": list(config.criteria.employment_types),
            "required_terms": list(config.criteria.required_terms),
            "industries": list(config.criteria.industries),
            "salary_ranges": list(config.criteria.salary_ranges),
            "company_types": list(config.criteria.company_types),
            "company_sizes": list(config.criteria.company_sizes),
            "position_levels": list(config.criteria.position_levels),
            "majors": list(config.criteria.majors),
            "certifications": list(config.criteria.certifications),
            "preferred_conditions": list(config.criteria.preferred_conditions),
            "welfare": list(config.criteria.welfare),
            "skills": list(config.criteria.skills),
            "tags": list(config.criteria.tags),
            "workplace_types": list(config.criteria.workplace_types),
            "date_posted": list(config.criteria.date_posted),
            "deadline": list(config.criteria.deadline),
            "easy_apply": list(config.criteria.easy_apply),
            "applicant_signals": list(config.criteria.applicant_signals),
            "network_signals": list(config.criteria.network_signals),
            "leader_positions": list(config.criteria.leader_positions),
            "headhunting": list(config.criteria.headhunting),
            "theme_tags": list(config.criteria.theme_tags),
            "extra_terms": list(config.criteria.extra_terms),
            "strict_match_groups": list(config.criteria.strict_match_groups),
        },
        "schedule": {
            "enabled": config.schedule.enabled,
            "timezone": config.schedule.timezone,
            "mode": config.schedule.mode,
            "times": list(config.schedule.times),
            "interval_hours": config.schedule.interval_hours,
            "run_on_start": config.schedule.run_on_start,
            "max_runs": config.schedule.max_runs,
        },
        "preprocessing": {
            "enabled": config.preprocessing.enabled,
            "dedupe_strategy": config.preprocessing.dedupe_strategy,
            "min_text_chars": config.preprocessing.min_text_chars,
            "normalize_whitespace": config.preprocessing.normalize_whitespace,
            "language_hints": list(config.preprocessing.language_hints),
        },
        "ai": {
            "auth_mode": config.ai.auth_mode,
            "api_key_env": config.ai.api_key_env,
            "oauth_profile": config.ai.oauth_profile,
            "external_command": config.ai.external_command,
            "config": dict(config.ai.config),
        },
        "integrations": {
            "harness_config": dict(config.integrations.harness_config),
            "mcp_servers": dict(config.integrations.mcp_servers),
            "skills_config": dict(config.integrations.skills_config),
            "messaging_config": dict(config.integrations.messaging_config),
            "contact_email_enabled": config.integrations.contact_email_enabled,
            "contact_email_from": config.integrations.contact_email_from,
            "contact_default_recipients": list(config.integrations.contact_default_recipients),
            "contact_message_template": config.integrations.contact_message_template,
        },
    }


def dump_config(path: str | Path, config: AppConfig) -> None:
    config_path = Path(path).expanduser().resolve()
    payload = config_to_dict(config)
    config_path.write_text(
        yaml.safe_dump(payload, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )


def build_queries(criteria: CriteriaConfig, manual_queries: list[str]) -> list[str]:
    if manual_queries:
        return _dedupe([query for query in manual_queries if query.strip()])

    shared_terms = _dedupe(
        criteria.keywords
        + criteria.locations
        + criteria.companies
        + criteria.experience_levels
        + criteria.education_levels
        + criteria.employment_types
        + criteria.industries
        + criteria.salary_ranges
        + criteria.company_types
        + criteria.company_sizes
        + criteria.position_levels
        + criteria.majors
        + criteria.certifications
        + criteria.preferred_conditions
        + criteria.welfare
        + criteria.skills
        + criteria.tags
        + criteria.workplace_types
        + criteria.date_posted
        + criteria.deadline
        + criteria.easy_apply
        + criteria.applicant_signals
        + criteria.network_signals
        + criteria.leader_positions
        + criteria.headhunting
        + criteria.theme_tags
        + criteria.required_terms
        + criteria.extra_terms
    )

    seeds = (
        criteria.roles
        or criteria.skills
        or criteria.tags
        or criteria.industries
        or criteria.position_levels
        or criteria.companies
        or criteria.required_terms
        or ["채용 공고"]
    )
    queries = []
    for seed in seeds[:8]:
        suffix = [term for term in shared_terms if term.casefold() != seed.casefold()]
        queries.append(" ".join([seed, *suffix[:6]]).strip())
    return _dedupe(queries)


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    unique: list[str] = []
    for value in values:
        cleaned = " ".join(value.split())
        if not cleaned:
            continue
        marker = cleaned.casefold()
        if marker in seen:
            continue
        seen.add(marker)
        unique.append(cleaned)
    return unique
