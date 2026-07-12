"""Run deterministic Norwegian public-sector language governance checks."""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


BASE_DIR = Path(__file__).resolve().parent
RULES_PATH = BASE_DIR / "rules.yaml"
EXAMPLES_DIR = BASE_DIR / "examples"
REPORT_PATH = BASE_DIR / "LANGUAGE_CONTROL_REPORT.md"
DISCLAIMER = (
    "These are deterministic early-warning checks. The report does not determine\n"
    "legal compliance, final linguistic correctness or whether a publication is\n"
    "suitable for a specific audience."
)
READY = "Ready for editorial review"
HUMAN_REVIEW = "Human language review required"
REVISION = "Revision required before publication"


class MetadataError(ValueError):
    """Raised when Markdown front matter is missing or invalid."""


@dataclass(frozen=True)
class Document:
    """Parsed Markdown with required governance metadata."""

    path: Path
    metadata: dict[str, Any]
    body: str

    @property
    def document_id(self) -> str:
        """Return the stable document identifier."""

        return str(self.metadata["document_id"])

    @property
    def file_name(self) -> str:
        """Return the source file name."""

        return self.path.name

    @property
    def title(self) -> str:
        """Return the document title."""

        return str(self.metadata["title"])


@dataclass(frozen=True)
class Finding:
    """One deterministic language-control result."""

    document_id: str
    file_name: str
    control_id: str
    rule_title: str
    severity: str
    evidence: str
    line_number: int | None
    why_it_matters: str
    suggested_action: str
    human_review_required: bool


def load_rules(path: Path = RULES_PATH) -> dict[str, Any]:
    """Load controls and deterministic keyword rules."""

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise MetadataError("rules.yaml must contain a mapping.")
    return data


def validate_metadata(name: str, metadata: dict[str, Any], required: list[str]) -> None:
    """Validate required front-matter fields and boolean types."""

    missing = [key for key in required if key not in metadata or metadata[key] in ("", None)]
    if missing:
        raise MetadataError(f"{name}: missing required metadata field(s): {', '.join(missing)}")
    for key in ("citizen_facing", "requires_next_step", "human_review_required"):
        if not isinstance(metadata[key], bool):
            raise MetadataError(f"{name}: {key} must be true or false.")


def parse_front_matter(path: Path, required_fields: list[str]) -> Document:
    """Parse YAML front matter and body from one Markdown file."""

    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise MetadataError(f"{path.name}: missing YAML front matter.")
    try:
        _, front_matter, body = text.split("---\n", 2)
    except ValueError as exc:
        raise MetadataError(f"{path.name}: invalid YAML front matter block.") from exc
    metadata = yaml.safe_load(front_matter)
    if not isinstance(metadata, dict):
        raise MetadataError(f"{path.name}: front matter must be a mapping.")
    validate_metadata(path.name, metadata, required_fields)
    return Document(path=path, metadata=metadata, body=body.strip())


def load_documents(
    examples_dir: Path = EXAMPLES_DIR, rules: dict[str, Any] | None = None
) -> list[Document]:
    """Load example documents in a stable order."""

    active_rules = rules or load_rules()
    required = list(active_rules["metadata_required"])
    return [parse_front_matter(path, required) for path in sorted(examples_dir.glob("*.md"))]


def control_map(rules: dict[str, Any]) -> dict[str, dict[str, str]]:
    """Return controls indexed by control ID."""

    return {str(item["id"]): item for item in rules["controls"]}


def line_for(text: str, evidence: str) -> int | None:
    """Find the first 1-based line number for evidence."""

    needle = evidence.lower()
    for index, line in enumerate(text.splitlines(), start=1):
        if needle in line.lower():
            return index
    return None


def finding(
    document: Document,
    rules: dict[str, Any],
    control_id: str,
    severity: str,
    evidence: str,
    suggested_action: str,
    human_review_required: bool,
    line_number: int | None = None,
) -> Finding:
    """Create a finding enriched with control text."""

    control = control_map(rules)[control_id]
    return Finding(
        document.document_id,
        document.file_name,
        control_id,
        str(control["title"]),
        severity,
        evidence,
        line_number if line_number is not None else line_for(document.body, evidence),
        str(control["why_it_matters"]),
        suggested_action,
        human_review_required,
    )


def has_token(text: str, token: str) -> bool:
    """Return whether a case-sensitive token appears as a word-like item."""

    return token in text.replace(".", " ").replace(",", " ").replace(":", " ").split()


def indicator_hits(text: str, indicators: list[str]) -> list[str]:
    """Return whole-word written-standard indicators found in text."""

    lowered = text.lower()
    return [
        item
        for item in indicators
        if re.search(r"(?<!\w)" + re.escape(item.lower()) + r"(?!\w)", lowered)
    ]


def check_written_standard(document: Document, rules: dict[str, Any]) -> list[Finding]:
    """Detect mixed Bokmål/Nynorsk indicators and metadata mismatch."""

    indicators = rules["written_standard_indicators"]
    bokmal = indicator_hits(document.body, list(indicators["bokmal"]))
    nynorsk = indicator_hits(document.body, list(indicators["nynorsk"]))
    results: list[Finding] = []
    if bokmal and nynorsk:
        results.append(
            finding(
                document,
                rules,
                "LNG-03",
                "medium",
                ", ".join(sorted(set(bokmal + nynorsk))),
                "Route the text to human language review and choose one written-standard strategy.",
                True,
                line_for(document.body, bokmal[0]) or line_for(document.body, nynorsk[0]),
            )
        )
    standard = str(document.metadata["language_standard"]).lower()
    if "bokmål" in standard and nynorsk:
        results.append(
            finding(
                document,
                rules,
                "LNG-03",
                "medium",
                ", ".join(sorted(set(nynorsk))),
                "Align the body text with the front-matter language_standard or update the metadata after review.",
                True,
                line_for(document.body, nynorsk[0]),
            )
        )
    return results


def check_document(document: Document, rules: dict[str, Any]) -> list[Finding]:
    """Run all deterministic checks for one document."""

    body = document.body
    lowered = body.lower()
    results: list[Finding] = []
    if has_token(body, "NAV") and has_token(body, "Nav"):
        results.append(
            finding(document, rules, "LNG-02", "low", "NAV / Nav", "Use NAV consistently when referring to the service name.", False, line_for(body, "Nav"))
        )
    results.extend(check_written_standard(document, rules))
    if "sammendrag:" not in lowered and "samandrag:" not in lowered:
        results.append(
            finding(document, rules, "LNG-04", "medium", "No plain-language summary heading found", "Add a short summary that states the main message in plain language.", True)
        )
    if document.metadata["requires_next_step"] and "neste steg:" not in lowered and "kva skjer vidare:" not in lowered:
        results.append(
            finding(document, rules, "LNG-05", "medium", "requires_next_step is true, but no next-step text was found", "Add a clear next step for the reader before publication.", True)
        )
    for item in rules["bureaucratic_terms"]:
        if str(item["term"]).lower() in lowered:
            results.append(
                finding(document, rules, "LNG-08", "low", str(item["term"]), str(item["suggestion"]), False)
            )
    for phrase in rules["vague_timing"]:
        if str(phrase).lower() in lowered:
            results.append(
                finding(document, rules, "LNG-06", "low", str(phrase), "Replace vague timing with a concrete date, deadline or service interval.", False)
            )
    for phrase in rules["responsibility_warnings"]:
        if str(phrase).lower() in lowered:
            results.append(
                finding(document, rules, "LNG-06", "medium", str(phrase), "Name the responsible unit or role so the reader knows who is accountable.", True)
            )
    for phrase in rules["passive_patterns"]:
        if str(phrase).lower() in lowered:
            results.append(
                finding(document, rules, "LNG-06", "medium", str(phrase), "Rewrite with a named actor where responsibility matters.", True)
            )
    if document.metadata["citizen_facing"]:
        for marker in rules["internal_markers"]:
            if str(marker).lower() in lowered:
                results.append(
                    finding(document, rules, "LNG-07", "high", str(marker), "Remove internal workflow notes from citizen-facing text before publication.", True)
                )
    if any(item.severity == "high" for item in results) and not document.metadata["human_review_required"]:
        results.append(
            finding(document, rules, "HUM-01", "high", "human_review_required: false", "Set human_review_required to true and route high-severity findings to an accountable reviewer.", True)
        )
    return results


def analyse_document(document: Document, rules: dict[str, Any]) -> list[Finding]:
    """Compatibility wrapper for tests and callers."""

    return check_document(document, rules)


def check_next_step(document: Document, rules: dict[str, Any]) -> list[Finding]:
    """Expose the next-step check for targeted tests."""

    lowered = document.body.lower()
    if not document.metadata["requires_next_step"] or "neste steg:" in lowered or "kva skjer vidare:" in lowered:
        return []
    return [
        finding(document, rules, "LNG-05", "medium", "requires_next_step is true, but no next-step text was found", "Add a clear next step for the reader before publication.", True)
    ]


def readiness_status(findings: list[Finding]) -> str:
    """Return the deterministic publication-readiness status."""

    if any(item.severity == "high" for item in findings):
        return REVISION
    if any(item.severity == "medium" and item.human_review_required for item in findings):
        return HUMAN_REVIEW
    return READY


def table(headers: list[str], rows: list[list[str]]) -> str:
    """Render a Markdown table."""

    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines)


def render_report(documents: list[Document], findings_by_doc: dict[str, list[Finding]]) -> str:
    """Render the deterministic language-control report."""

    all_findings = [item for doc in documents for item in findings_by_doc[doc.document_id]]
    severities = Counter(item.severity for item in all_findings)
    controls = Counter(item.control_id for item in all_findings)
    readiness_rows = [[doc.document_id, doc.file_name, readiness_status(findings_by_doc[doc.document_id])] for doc in documents]
    review_rows = [row for row in readiness_rows if row[2] != READY] or [["None", "None", READY]]
    parts = [
        "# Norwegian Public-Sector Language Control Report",
        "",
        "## Executive Summary",
        "",
        f"Documents checked: {len(documents)}",
        "",
        f"Total findings: {len(all_findings)}",
        "",
        "This report applies deterministic early-warning controls to fictional Norwegian public-sector text examples. It supports accountable human review, controlled multilingual communication and publication-readiness discussions.",
        "",
        "## Findings by Severity",
        "",
        table(["Severity", "Count"], [[level, str(severities.get(level, 0))] for level in ["info", "low", "medium", "high"]]),
        "",
        "## Findings by Control ID",
        "",
        table(["Control ID", "Count"], [[key, str(controls[key])] for key in sorted(controls)]),
        "",
        "## Publication-Readiness Overview",
        "",
        table(["Document ID", "File", "Status"], readiness_rows),
        "",
        "## Human-Review Queue",
        "",
        table(["Document ID", "File", "Status"], review_rows),
        "",
    ]
    for doc in documents:
        findings = findings_by_doc[doc.document_id]
        parts.extend([
            f"## {doc.title}",
            "",
            f"- Document ID: `{doc.document_id}`",
            f"- File: `{doc.file_name}`",
            f"- Intended audience: {doc.metadata['intended_audience']}",
            f"- Language standard: {doc.metadata['language_standard']}",
            f"- Publication channel: {doc.metadata['publication_channel']}",
            f"- Citizen-facing: {doc.metadata['citizen_facing']}",
            f"- Requires next step: {doc.metadata['requires_next_step']}",
            f"- Content owner: {doc.metadata['content_owner']}",
            f"- Human review required: {doc.metadata['human_review_required']}",
            f"- Publication-readiness status: {readiness_status(findings)}",
            "",
        ])
        if not findings:
            parts.extend(["Clean-baseline result: no findings were produced for this document.", ""])
            continue
        rows = [[item.control_id, item.rule_title, item.severity, item.evidence, str(item.line_number or "Not line-specific"), item.suggested_action, str(item.human_review_required)] for item in findings]
        parts.extend([table(["Control ID", "Rule title", "Severity", "Evidence", "Line", "Suggested action", "Human review"], rows), ""])
        parts.extend([f"- Why {item.control_id} matters: {item.why_it_matters}" for item in findings])
        parts.append("")
    parts.extend(["## Disclaimer", "", DISCLAIMER, ""])
    return "\n".join(parts)


def run_checks() -> tuple[list[Document], dict[str, list[Finding]], str]:
    """Load inputs, run checks and write the report."""

    rules = load_rules()
    documents = load_documents(rules=rules)
    findings_by_doc = {doc.document_id: analyse_document(doc, rules) for doc in documents}
    report = render_report(documents, findings_by_doc)
    REPORT_PATH.write_text(report, encoding="utf-8")
    return documents, findings_by_doc, report


def main() -> None:
    """Run checks from the command line."""

    documents, findings_by_doc, _ = run_checks()
    total = sum(len(items) for items in findings_by_doc.values())
    print(f"Wrote {REPORT_PATH.relative_to(Path.cwd())}")
    print(f"Checked {len(documents)} documents with {total} finding(s)")


if __name__ == "__main__":
    main()
