"""Run a deterministic grounded-answer transparency demo."""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


BASE_DIR = Path(__file__).resolve().parent
SOURCES_DIR = BASE_DIR / "approved_sources"
QUESTIONS_PATH = BASE_DIR / "questions.yaml"
REPORT_PATH = BASE_DIR / "ANSWER_LOG.md"
AUDIT_RUN_ID = "CN-GROUNDING-DEMO-2026-07-01"
CONTROL_IDS = ["RAG-01", "RAG-02", "RAG-03", "AUD-02", "HUM-01"]
DISCLAIMER = (
    "This deterministic demonstration supports early governance and assurance\n"
    "work. It does not provide legal advice, compliance certification, a final\n"
    "procurement decision, a DPIA, a security approval or a production-readiness\n"
    "determination."
)
STOPWORDS = {"the", "and", "or", "is", "are", "i", "my", "can", "what", "when", "with", "by", "to", "me", "from", "a", "an"}


class GroundingError(ValueError):
    """Raised when grounding demo inputs are invalid."""


@dataclass(frozen=True)
class Source:
    """Approved source document."""

    source_id: str
    title: str
    topic: str
    body: str
    path: Path


def parse_source(path: Path) -> Source:
    """Parse a source Markdown file with YAML front matter."""

    text = path.read_text(encoding="utf-8")
    _, meta_text, body = text.split("---\n", 2)
    meta = yaml.safe_load(meta_text)
    return Source(str(meta["source_id"]), str(meta["title"]), str(meta["approved_topic"]), body.strip(), path)


def load_sources() -> list[Source]:
    """Load approved sources in stable order."""

    return [parse_source(path) for path in sorted(SOURCES_DIR.glob("*.md"))]


def load_questions(path: Path = QUESTIONS_PATH) -> list[dict[str, Any]]:
    """Load and validate questions."""

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    questions = data.get("questions") if isinstance(data, dict) else None
    if not isinstance(questions, list):
        raise GroundingError("questions.yaml must contain questions.")
    required = {"id", "question", "intended_topic", "requires_human_review", "minimum_support_threshold"}
    for item in questions:
        missing = required - set(item)
        if missing:
            raise GroundingError(f"{item.get('id', 'question')} missing fields: {', '.join(sorted(missing))}")
    return questions


def tokens(text: str) -> set[str]:
    """Tokenise text for deterministic matching."""

    return {token for token in re.findall(r"[A-Za-z0-9-]+", text.lower()) if token not in STOPWORDS and len(token) > 2}


def matched_evidence(question: dict[str, Any], source: Source) -> list[str]:
    """Return matched question terms appearing in source body."""

    q_tokens = tokens(str(question["question"]))
    body_tokens = tokens(source.body)
    return sorted(q_tokens & body_tokens)


def predefined_answer(question_id: str) -> str:
    """Return deterministic approved answer template."""

    answers = {
        "q1-service-hours": "The service centre is open Monday to Friday from 09:00 to 15:00.",
        "q2-secure-documents": "No. Documents containing personal information should be submitted through the secure document portal, not ordinary email.",
        "q3-appeal-guidance": "Automated tools must not decide whether an appeal will succeed. General appeal information is normally found in the written decision letter.",
    }
    return answers[question_id]


def assess_question(question: dict[str, Any], sources: list[Source]) -> dict[str, Any]:
    """Assess one question against approved sources."""

    related = [source for source in sources if source.topic == question["intended_topic"]]
    if not related:
        return result(question, "Refused: no approved source", "No approved source covers this topic.", [], [], 0.0)
    source = related[0]
    evidence = matched_evidence(question, source)
    threshold = int(question["minimum_support_threshold"])
    if len(evidence) >= threshold and str(question["id"]) in {"q1-service-hours", "q2-secure-documents", "q3-appeal-guidance"}:
        outcome = "Escalated for human review" if question["requires_human_review"] else "Answered from approved source"
        answer = predefined_answer(str(question["id"]))
        return result(question, outcome, answer, [source], evidence, min(0.95, 0.5 + len(evidence) / 10))
    return result(question, "Refused: insufficient source support", "The related source does not support a precise answer to this question.", [source], evidence, min(0.49, len(evidence) / max(threshold, 1)))


def result(question: dict[str, Any], outcome: str, answer: str, sources: list[Source], evidence: list[str], confidence: float) -> dict[str, Any]:
    """Build a stable answer-log result."""

    return {
        "question_id": question["id"],
        "question": question["question"],
        "outcome": outcome,
        "answer": answer,
        "approved_sources": [source.source_id for source in sources],
        "matched_evidence": evidence,
        "support_assessment": f"{len(evidence)} matched term(s); threshold {question['minimum_support_threshold']}",
        "confidence": round(confidence, 2),
        "limitations": "Topical relevance is not enough; the specific answer must be supported by approved text.",
        "human_review_requirement": bool(question["requires_human_review"]) or outcome.startswith("Escalated"),
        "control_ids": CONTROL_IDS,
        "audit_run_id": AUDIT_RUN_ID,
    }


def render_report(results: list[dict[str, Any]]) -> str:
    """Render the deterministic answer log."""

    counts = Counter(item["outcome"] for item in results)
    lines = [
        "# Grounded Answer Transparency Log",
        "",
        "## Executive Summary",
        "",
        f"Audit run ID: {AUDIT_RUN_ID}",
        "",
        f"Questions checked: {len(results)}",
        "",
        "This log demonstrates deterministic refusal when approved sources do not support a specific answer.",
        "",
        "## Counts By Outcome",
        "",
        "| Outcome | Count |",
        "| --- | ---: |",
        *[f"| {outcome} | {counts[outcome]} |" for outcome in sorted(counts)],
        "",
    ]
    for item in results:
        lines.extend([
            f"## {item['question_id']}",
            "",
            f"- Question: {item['question']}",
            f"- Outcome: {item['outcome']}",
            f"- Answer or refusal: {item['answer']}",
            f"- Approved sources: {', '.join(item['approved_sources']) if item['approved_sources'] else 'None'}",
            f"- Matched evidence: {', '.join(item['matched_evidence']) if item['matched_evidence'] else 'None'}",
            f"- Support assessment: {item['support_assessment']}",
            f"- Confidence: {item['confidence']}",
            f"- Limitations: {item['limitations']}",
            f"- Human-review requirement: {item['human_review_requirement']}",
            f"- Control IDs: {', '.join(item['control_ids'])}",
            f"- Audit run ID: {item['audit_run_id']}",
            "",
        ])
    lines.extend(["## Disclaimer", "", DISCLAIMER, ""])
    return "\n".join(lines)


def run_demo() -> tuple[list[dict[str, Any]], str]:
    """Run the demo and write the answer log."""

    sources = load_sources()
    questions = load_questions()
    results = [assess_question(question, sources) for question in questions]
    report = render_report(results)
    REPORT_PATH.write_text(report, encoding="utf-8")
    return results, report


def main() -> None:
    """CLI entry point."""

    results, _ = run_demo()
    counts = Counter(item["outcome"] for item in results)
    print(f"Wrote {REPORT_PATH.relative_to(Path.cwd())}")
    print("Outcome counts: " + ", ".join(f"{key}={counts[key]}" for key in sorted(counts)))


if __name__ == "__main__":
    main()
