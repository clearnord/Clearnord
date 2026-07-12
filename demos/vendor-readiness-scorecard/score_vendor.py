"""Generate a deterministic public-sector AI vendor readiness scorecard."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml


BASE_DIR = Path(__file__).resolve().parent
QUESTIONNAIRE_PATH = BASE_DIR / "questionnaire.yaml"
ANSWERS_PATH = BASE_DIR / "sample_vendor_answers.yaml"
REPORT_PATH = BASE_DIR / "VENDOR_SCORECARD.md"
DISCLAIMER = (
    "This deterministic demonstration supports early governance and assurance\n"
    "work. It does not provide legal advice, compliance certification, a final\n"
    "procurement decision, a DPIA, a security approval or a production-readiness\n"
    "determination."
)
GREEN = "Green: acceptable for a controlled pilot, subject to ordinary approvals"
YELLOW = "Yellow: clarification or compensating controls required before pilot"
RED = "Red: not ready for public-sector pilot"


class ScorecardError(ValueError):
    """Raised when scorecard input is invalid."""


def load_yaml(path: Path) -> dict[str, Any]:
    """Load YAML as a mapping."""

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ScorecardError(f"{path.name} must contain a mapping.")
    return data


def questionnaire(data: dict[str, Any]) -> list[dict[str, Any]]:
    """Return validated questionnaire items."""

    questions = data.get("questions")
    if not isinstance(questions, list) or not questions:
        raise ScorecardError("questionnaire.yaml must contain questions.")
    required = {"id", "control_id", "domain", "question", "weight", "acceptable_answers", "evidence_required", "hard_stop_condition", "rationale", "scores"}
    for question in questions:
        missing = sorted(required - set(question))
        if missing:
            raise ScorecardError(f"{question.get('id', 'question')} missing fields: {', '.join(missing)}")
    return questions


def answer_map(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Return validated answer mapping."""

    answers = data.get("answers")
    if not isinstance(answers, dict):
        raise ScorecardError("sample_vendor_answers.yaml must contain answers.")
    return answers


def validate_answers(questions: list[dict[str, Any]], answers: dict[str, dict[str, Any]]) -> list[str]:
    """Detect missing and unsupported answers."""

    missing: list[str] = []
    for question in questions:
        qid = str(question["id"])
        if qid not in answers:
            missing.append(qid)
            continue
        value = answers[qid].get("answer")
        if value not in question["acceptable_answers"]:
            raise ScorecardError(f"{qid} has unsupported answer value: {value}")
    return missing


def detect_hard_stops(questions: list[dict[str, Any]], answers: dict[str, dict[str, Any]]) -> list[str]:
    """Return hard-stop question IDs triggered by answers."""

    stops: list[str] = []
    for question in questions:
        stop_value = question.get("hard_stop_condition")
        if stop_value is not None and answers.get(str(question["id"]), {}).get("answer") == stop_value:
            stops.append(str(question["id"]))
    return stops


def score(questions: list[dict[str, Any]], answers: dict[str, dict[str, Any]]) -> tuple[float, dict[str, float]]:
    """Calculate weighted score and domain percentages."""

    total_weight = 0.0
    achieved = 0.0
    domain_weight: dict[str, float] = defaultdict(float)
    domain_score: dict[str, float] = defaultdict(float)
    for question in questions:
        qid = str(question["id"])
        if qid not in answers:
            continue
        weight = float(question["weight"])
        value = answers[qid]["answer"]
        points = float(question["scores"][value]) * weight
        total_weight += weight
        achieved += points
        domain = str(question["domain"])
        domain_weight[domain] += weight
        domain_score[domain] += points
    overall = round((achieved / total_weight) * 100, 1) if total_weight else 0.0
    domains = {domain: round((domain_score[domain] / weight) * 100, 1) for domain, weight in domain_weight.items()}
    return overall, domains


def result_for(score_value: float, hard_stops: list[str]) -> str:
    """Return traffic-light result, with hard stops overriding score."""

    if hard_stops:
        return RED
    if score_value >= 80:
        return GREEN
    if score_value >= 60:
        return YELLOW
    return RED


def evidence_gaps(answers: dict[str, dict[str, Any]]) -> list[str]:
    """List answers with partial, missing or weak evidence."""

    gaps: list[str] = []
    for qid, answer in answers.items():
        quality = str(answer.get("evidence_quality", ""))
        value = str(answer.get("answer", ""))
        if quality in {"vendor_statement", "partial_document", ""} or value in {"partial", "incomplete", "limited_notice", "needs_clarification", "deletion_only", "mixed"}:
            gaps.append(qid)
    return sorted(gaps)


def collect_field(answers: dict[str, dict[str, Any]], field: str) -> list[str]:
    """Collect non-empty answer field values as report bullets."""

    items = [f"{qid}: {value}" for qid, answer in sorted(answers.items()) if (value := answer.get(field))]
    return items


def render_report(vendor_data: dict[str, Any], qdata: dict[str, Any], questions: list[dict[str, Any]], answers: dict[str, dict[str, Any]]) -> str:
    """Render the Markdown scorecard."""

    missing = validate_answers(questions, answers)
    hard_stops = detect_hard_stops(questions, answers)
    score_value, domain_scores = score(questions, answers)
    result = result_for(score_value, hard_stops)
    vendor = vendor_data["vendor"]
    supplied = collect_field(answers, "evidence")
    gaps = evidence_gaps(answers)
    clarifications = collect_field(answers, "clarification")
    safeguards = collect_field(answers, "safeguard")
    rows = []
    for question in questions:
        qid = str(question["id"])
        value = answers.get(qid, {}).get("answer", "UNANSWERED")
        rows.append(f"| {qid} | {question['control_id']} | {question['domain']} | {value} | {question['weight']} |")
    domain_rows = [f"| {domain} | {value:.1f} |" for domain, value in sorted(domain_scores.items())]
    next_step = "Resolve evidence gaps and contractual clarifications before any controlled pilot."
    return "\n".join([
        "# Vendor Readiness Scorecard",
        "",
        "## Executive Summary",
        "",
        f"Vendor name: {vendor['name']}",
        "",
        f"Fictional assessment ID: {vendor['assessment_id']}",
        "",
        f"Traffic-light result: {result}",
        "",
        f"Weighted score: {score_value:.1f}",
        "",
        f"Hard-stop summary: {', '.join(hard_stops) if hard_stops else 'No hard stops triggered.'}",
        "",
        "## Score By Control Domain",
        "",
        "| Domain | Score |",
        "| --- | ---: |",
        *domain_rows,
        "",
        "## Detailed Question Results",
        "",
        "| Question ID | Control ID | Domain | Answer | Weight |",
        "| --- | --- | --- | --- | ---: |",
        *rows,
        "",
        "## Evidence Supplied",
        "",
        *(f"- {item}" for item in supplied),
        "",
        "## Missing Or Weak Evidence",
        "",
        *(f"- {item}" for item in gaps),
        "",
        "## Unanswered Questions",
        "",
        *(f"- {item}" for item in (missing or ["None"])),
        "",
        "## Required Clarification Before Pilot",
        "",
        *(f"- {item}" for item in clarifications),
        "",
        "## Suggested Contractual Safeguards",
        "",
        *(f"- {item}" for item in safeguards),
        "",
        "## Recommended Next Step",
        "",
        next_step,
        "",
        "## Disclaimer",
        "",
        DISCLAIMER,
        "",
    ])


def generate_scorecard() -> tuple[str, str, float]:
    """Generate the scorecard and return report, result and score."""

    qdata = load_yaml(QUESTIONNAIRE_PATH)
    adata = load_yaml(ANSWERS_PATH)
    questions = questionnaire(qdata)
    answers = answer_map(adata)
    validate_answers(questions, answers)
    report = render_report(adata, qdata, questions, answers)
    REPORT_PATH.write_text(report, encoding="utf-8")
    hard_stops = detect_hard_stops(questions, answers)
    score_value, _ = score(questions, answers)
    return report, result_for(score_value, hard_stops), score_value


def main() -> None:
    """CLI entry point."""

    _, result, score_value = generate_scorecard()
    print(f"Wrote {REPORT_PATH.relative_to(Path.cwd())}")
    print(f"Result: {result}")
    print(f"Weighted score: {score_value:.1f}")


if __name__ == "__main__":
    main()
