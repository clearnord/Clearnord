"""Tests for the vendor readiness scorecard demo."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "score_vendor.py"
SPEC = importlib.util.spec_from_file_location("score_vendor", SCRIPT)
assert SPEC and SPEC.loader
score_vendor = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = score_vendor
SPEC.loader.exec_module(score_vendor)


def sample() -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    """Load questionnaire and answers."""

    questions = score_vendor.questionnaire(score_vendor.load_yaml(score_vendor.QUESTIONNAIRE_PATH))
    answers = score_vendor.answer_map(score_vendor.load_yaml(score_vendor.ANSWERS_PATH))
    return questions, answers


def test_missing_answer_is_detected() -> None:
    """Missing answers are returned explicitly."""

    questions, answers = sample()
    answers.pop("processing_location")
    assert "processing_location" in score_vendor.validate_answers(questions, answers)


def test_unsupported_answer_value_raises_clear_error() -> None:
    """Unsupported answer values fail validation."""

    questions, answers = sample()
    answers["processing_location"]["answer"] = "maybe"
    with pytest.raises(score_vendor.ScorecardError, match="unsupported answer"):
        score_vendor.validate_answers(questions, answers)


def test_shared_model_training_triggers_red() -> None:
    """Shared-model training is a hard stop."""

    questions, answers = sample()
    answers["customer_data_training"]["answer"] = "shared_training"
    stops = score_vendor.detect_hard_stops(questions, answers)
    assert score_vendor.result_for(100.0, stops).startswith("Red")


def test_unknown_processing_location_triggers_red() -> None:
    """Unknown processing location is a hard stop."""

    questions, answers = sample()
    answers["processing_location"]["answer"] = "unknown"
    stops = score_vendor.detect_hard_stops(questions, answers)
    assert "processing_location" in stops


def test_missing_security_documentation_triggers_red() -> None:
    """Unavailable security documentation is a hard stop."""

    questions, answers = sample()
    answers["security_documentation"]["answer"] = "unavailable"
    stops = score_vendor.detect_hard_stops(questions, answers)
    assert score_vendor.result_for(99.0, stops).startswith("Red")


def test_partial_evidence_can_produce_yellow() -> None:
    """The sample contains enough partial evidence to produce Yellow."""

    questions, answers = sample()
    value, _ = score_vendor.score(questions, answers)
    result = score_vendor.result_for(value, score_vendor.detect_hard_stops(questions, answers))
    assert result.startswith("Yellow")


def test_high_score_cannot_override_hard_stop() -> None:
    """Hard stops override the weighted score."""

    assert score_vendor.result_for(100.0, ["incident_notification"]).startswith("Red")


def test_generated_scorecard_contains_all_control_domains() -> None:
    """Rendered report includes every questionnaire domain."""

    qdata = score_vendor.load_yaml(score_vendor.QUESTIONNAIRE_PATH)
    adata = score_vendor.load_yaml(score_vendor.ANSWERS_PATH)
    questions = score_vendor.questionnaire(qdata)
    report = score_vendor.render_report(adata, qdata, questions, score_vendor.answer_map(adata))
    for domain in sorted({question["domain"] for question in questions}):
        assert domain in report
