"""Tests for the grounded-answer transparency demo."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "run_grounding_demo.py"
SPEC = importlib.util.spec_from_file_location("run_grounding_demo", SCRIPT)
assert SPEC and SPEC.loader
grounding = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = grounding
SPEC.loader.exec_module(grounding)


def result(question_id: str) -> dict:
    """Return one assessment result."""

    sources = grounding.load_sources()
    for question in grounding.load_questions():
        if question["id"] == question_id:
            return grounding.assess_question(question, sources)
    raise AssertionError(question_id)


def test_approved_source_is_retrieved() -> None:
    """Approved source documents are loaded."""

    assert any(source.source_id == "service-centre-contact" for source in grounding.load_sources())


def test_supported_question_is_answered() -> None:
    """Supported questions receive a predefined answer."""

    assert result("q1-service-hours")["outcome"] == "Answered from approved source"


def test_no_source_question_is_refused() -> None:
    """No-source questions are refused."""

    assert result("q4-building-processing-time")["outcome"] == "Refused: no approved source"


def test_related_but_insufficient_question_is_refused() -> None:
    """Related sources do not automatically support precise answers."""

    assert result("q5-specific-appeal-deadline")["outcome"] == "Refused: insufficient source support"


def test_source_reference_is_included() -> None:
    """Supported answers include source references."""

    assert result("q2-secure-documents")["approved_sources"] == ["secure-document-submission"]


def test_no_processing_time_is_invented() -> None:
    """The processing-time refusal does not invent a number."""

    answer = result("q4-building-processing-time")["answer"]
    assert "days" not in answer.lower() and "weeks" not in answer.lower()


def test_fixed_audit_run_id_is_used() -> None:
    """Audit run ID is deterministic."""

    assert result("q1-service-hours")["audit_run_id"] == "CN-GROUNDING-DEMO-2026-07-01"


def test_report_contains_all_questions() -> None:
    """Rendered report includes all configured question IDs."""

    results, report = grounding.run_demo()
    assert len(results) == 5
    for question in grounding.load_questions():
        assert question["id"] in report
