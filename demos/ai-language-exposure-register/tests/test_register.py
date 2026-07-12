"""Tests for the deterministic exposure register demo."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

import pytest


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "generate_register.py"
SPEC = importlib.util.spec_from_file_location("generate_register", SCRIPT_PATH)
assert SPEC is not None
register = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = register
SPEC.loader.exec_module(register)


def load_demo_systems() -> list[dict[str, Any]]:
    """Load the demo systems through the generator helpers."""

    data = register.load_yaml(register.SYSTEMS_PATH)
    return register.systems_from_data(data)


def schema() -> dict[str, Any]:
    """Load the demo schema."""

    return register.load_schema(register.SCHEMA_PATH)


def clone_system(system_id: str = "test-system") -> dict[str, Any]:
    """Return a mutable copy of a valid demo system."""

    system = dict(load_demo_systems()[0])
    system["id"] = system_id
    system["applicable_controls"] = list(system["applicable_controls"])
    system["target_users"] = list(system["target_users"])
    system["affected_groups"] = list(system["affected_groups"])
    system["languages"] = list(system["languages"])
    system["document_types"] = list(system["document_types"])
    system["data_categories"] = list(system["data_categories"])
    system["known_limitations"] = list(system["known_limitations"])
    system["mitigation_measures"] = list(system["mitigation_measures"])
    return system


def test_missing_required_field() -> None:
    """A missing required field is rejected."""

    system = clone_system()
    del system["purpose"]
    with pytest.raises(register.RegisterValidationError, match="purpose"):
        register.validate_required_fields([system], schema())


def test_duplicate_system_id() -> None:
    """Duplicate system IDs are rejected."""

    first = clone_system("duplicate-id")
    second = clone_system("duplicate-id")
    with pytest.raises(register.RegisterValidationError, match="Duplicate system id"):
        register.detect_duplicate_ids([first, second])


def test_invalid_approved_use_status() -> None:
    """Approved-use status must use the schema enum."""

    system = clone_system()
    system["approved_use_status"] = "Pilot maybe"
    with pytest.raises(register.RegisterValidationError, match="approved_use_status"):
        register.validate_enums([system], schema())


def test_special_category_data_produces_high_or_critical_priority() -> None:
    """Special-category data produces at least high priority."""

    system = clone_system()
    system["special_category_data"] = True
    system["personal_data"] = True
    priority = register.calculate_governance_priority(system)
    assert priority in {"High", "Critical"}


def test_missing_human_review_produces_control_gap() -> None:
    """Missing human review creates human oversight control gaps."""

    system = clone_system()
    system["human_review"] = "No approved human review workflow."
    system["authorised_approver"] = "None assigned"
    system["applicable_controls"] = [
        control
        for control in system["applicable_controls"]
        if not control.startswith("HUM-")
    ]
    analysis = register.analyse_system(system)
    assert "HUM-01" in analysis.missing_controls
    assert "HUM-02" in analysis.missing_controls
    assert analysis.missing_human_oversight is True


def test_overdue_next_review_date_is_detected() -> None:
    """Dates before the fixed reference date are overdue."""

    system = clone_system()
    system["next_review_date"] = "2026-06-30"
    assert register.is_overdue_review(system) is True


def test_generated_report_contains_all_four_systems() -> None:
    """The rendered report includes every demo system."""

    systems = load_demo_systems()
    report = register.render_report(register.analyse_systems(systems))
    assert "Internal document assistant" in report
    assert "Citizen-service chatbot" in report
    assert "Case-summary assistant" in report
    assert "Language simplification assistant" in report
