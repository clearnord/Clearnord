"""Tests for the red-team evaluation kit."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "run_evaluations.py"
SPEC = importlib.util.spec_from_file_location("run_evaluations", SCRIPT)
assert SPEC and SPEC.loader
evals = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = evals
SPEC.loader.exec_module(evals)


def test_missing_response_id_raises_clear_error() -> None:
    """Missing response IDs fail validation."""

    cases = [dict(evals.load_cases()[0], response_id="missing")]
    with pytest.raises(evals.EvaluationError, match="missing response_id"):
        evals.validate_response_ids(cases, evals.load_responses())


def test_must_contain_assertion() -> None:
    """must_contain finds missing text."""

    failures = evals.run_assertions({"automated_assertions": {"must_contain": ["needle"]}}, {"text": "haystack", "cited_sources": []}, set())
    assert failures


def test_must_not_contain_assertion() -> None:
    """must_not_contain detects prohibited text."""

    failures = evals.run_assertions({"automated_assertions": {"must_not_contain": ["secret"]}}, {"text": "secret text", "cited_sources": []}, set())
    assert failures


def test_refusal_assertion() -> None:
    """Refusal assertion passes on cannot wording."""

    failures = evals.run_assertions({"automated_assertions": {"must_refuse": True}}, {"text": "I cannot answer.", "cited_sources": []}, set())
    assert failures == []


def test_escalation_assertion() -> None:
    """Escalation assertion passes on human wording."""

    failures = evals.run_assertions({"automated_assertions": {"must_escalate": True}}, {"text": "Ask a human reviewer.", "cited_sources": []}, set())
    assert failures == []


def test_approved_source_assertion() -> None:
    """Approved-source assertion requires approved citations."""

    failures = evals.run_assertions({"automated_assertions": {"must_cite_approved_source": True}}, {"text": "Answer", "cited_sources": ["bad"]}, {"good"})
    assert failures


def test_release_blocking_high_failure_produces_release_blocked() -> None:
    """High release-blocking failures block release."""

    results, _ = evals.run()
    assert evals.release_recommendation(results) == evals.BLOCKED


def test_non_blocking_medium_failure_does_not_alone_produce_release_blocked() -> None:
    """A non-blocking medium failure alone requires remediation, not blocking."""

    result = [{"passed": False, "release_blocking": False, "severity": "medium"}]
    assert evals.release_recommendation(result) == evals.REMEDIATE


def test_generated_report_includes_all_test_cases() -> None:
    """Report includes every test ID."""

    results, report = evals.run()
    for item in results:
        assert item["id"] in report


def test_pass_rate_is_calculated_correctly() -> None:
    """Pass rate is deterministic."""

    results = [{"passed": True}, {"passed": False}, {"passed": True}, {"passed": False}]
    assert evals.pass_rate(results) == 50.0
