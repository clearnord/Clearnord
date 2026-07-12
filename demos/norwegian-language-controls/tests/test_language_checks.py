"""Tests for the Norwegian language-control demo."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

import pytest


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "run_language_checks.py"
SPEC = importlib.util.spec_from_file_location("run_language_checks", SCRIPT_PATH)
assert SPEC is not None
language_checks = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = language_checks
SPEC.loader.exec_module(language_checks)


def rules() -> dict[str, Any]:
    """Load demo rules."""

    return language_checks.load_rules()


def documents() -> list[Any]:
    """Load demo documents."""

    return language_checks.load_documents(rules=rules())


def document(document_id: str) -> Any:
    """Return a document by ID."""

    for item in documents():
        if item.document_id == document_id:
            return item
    raise AssertionError(f"Document not found: {document_id}")


def findings(document_id: str) -> list[Any]:
    """Return findings for one document."""

    return language_checks.analyse_document(document(document_id), rules())


def test_valid_yaml_front_matter_is_parsed() -> None:
    """A valid example returns expected metadata."""

    parsed = document("clear-service-notice")
    assert parsed.metadata["language_standard"] == "Bokmål"
    assert parsed.metadata["citizen_facing"] is True


def test_missing_required_metadata_raises_clear_error(tmp_path: Path) -> None:
    """Missing required front-matter metadata raises a clear error."""

    sample = tmp_path / "bad.md"
    sample.write_text(
        "---\n"
        "document_id: bad\n"
        "title: Bad\n"
        "language_standard: Bokmål\n"
        "publication_channel: Test\n"
        "citizen_facing: true\n"
        "requires_next_step: false\n"
        "content_owner: Test\n"
        "human_review_required: true\n"
        "---\n"
        "Body\n",
        encoding="utf-8",
    )
    with pytest.raises(language_checks.MetadataError, match="intended_audience"):
        language_checks.parse_front_matter(sample, rules()["metadata_required"])


def test_nav_and_nav_inconsistency_is_detected() -> None:
    """Mixed NAV/Nav capitalization creates a terminology finding."""

    result = findings("nav-capitalisation")
    assert any(item.control_id == "LNG-02" and "NAV" in item.evidence for item in result)


def test_mixed_bokmal_and_nynorsk_indicators_are_detected() -> None:
    """Mixed written-standard indicators require language review."""

    result = findings("mixed-bokmal-nynorsk")
    assert any(item.control_id == "LNG-03" and item.human_review_required for item in result)


def test_bureaucratic_wording_produces_suggested_alternative() -> None:
    """Bureaucratic terms include a suggested alternative."""

    result = findings("bureaucratic-internal-note")
    assert any(
        item.control_id == "LNG-08" and "Use" in item.suggested_action
        for item in result
    )


def test_missing_next_step_is_detected_only_when_required(tmp_path: Path) -> None:
    """Missing next step is reported only when requires_next_step is true."""

    base = document("clear-service-notice")
    required_doc = language_checks.Document(
        path=base.path,
        metadata={**base.metadata, "requires_next_step": True},
        body="Sammendrag: Kort tekst uten neste steg.",
    )
    optional_doc = language_checks.Document(
        path=base.path,
        metadata={**base.metadata, "requires_next_step": False},
        body="Sammendrag: Kort tekst uten neste steg.",
    )
    required = language_checks.check_next_step(required_doc, rules())
    optional = language_checks.check_next_step(optional_doc, rules())
    assert any(item.control_id == "LNG-05" for item in required)
    assert optional == []


def test_internal_note_in_citizen_facing_text_produces_high_finding() -> None:
    """Internal markers in public text are high severity."""

    result = findings("bureaucratic-internal-note")
    assert any(item.control_id == "LNG-07" and item.severity == "high" for item in result)


def test_vague_timing_is_detected() -> None:
    """Vague timing terms are reported."""

    result = findings("bureaucratic-internal-note")
    assert any(item.control_id == "LNG-06" and item.evidence == "senere" for item in result)


def test_unclear_or_passive_responsibility_is_detected() -> None:
    """Unclear responsibility and passive wording are reported."""

    result = findings("bureaucratic-internal-note")
    assert any("ansvarlig enhet" in item.evidence for item in result)
    assert any("bli behandlet" in item.evidence for item in result)


def test_clean_baseline_has_no_high_severity_findings() -> None:
    """The clean baseline has no high-severity findings."""

    result = findings("clear-service-notice")
    assert not any(item.severity == "high" for item in result)


def test_report_contains_all_four_example_documents() -> None:
    """The generated report includes every example document."""

    docs = documents()
    by_doc = {item.document_id: language_checks.analyse_document(item, rules()) for item in docs}
    report = language_checks.render_report(docs, by_doc)
    assert "01-clear-service-notice.md" in report
    assert "02-nav-capitalisation.md" in report
    assert "03-mixed-bokmal-nynorsk.md" in report
    assert "04-bureaucratic-internal-note.md" in report


def test_high_finding_produces_revision_required_status() -> None:
    """Any high finding produces the revision-required status."""

    result = findings("bureaucratic-internal-note")
    assert language_checks.readiness_status(result) == language_checks.REVISION
