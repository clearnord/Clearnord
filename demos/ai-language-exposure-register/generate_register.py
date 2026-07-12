"""Generate a deterministic AI and language exposure register.

The demo reads fictional municipal system records from ``systems.yaml``,
validates them against the local schema metadata, applies transparent
governance rules, and writes ``EXPOSURE_REGISTER.md``.
"""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import yaml


REFERENCE_DATE = date(2026, 7, 1)
BASE_DIR = Path(__file__).resolve().parent
SYSTEMS_PATH = BASE_DIR / "systems.yaml"
SCHEMA_PATH = BASE_DIR / "schema.json"
OUTPUT_PATH = BASE_DIR / "EXPOSURE_REGISTER.md"

CONTROL_IDS = {
    "GOV-01",
    "GOV-02",
    "GOV-03",
    "DAT-01",
    "DAT-02",
    "DAT-03",
    "HUM-01",
    "HUM-02",
    "HUM-03",
    "LNG-01",
    "LNG-02",
    "VEN-01",
    "VEN-02",
    "AUD-01",
    "AUD-02",
    "EVA-01",
}
PRIORITY_ORDER = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}


class RegisterValidationError(ValueError):
    """Raised when demo input data fails validation."""


@dataclass(frozen=True)
class SystemAnalysis:
    """Computed governance observations for one system."""

    system: dict[str, Any]
    calculated_priority: str
    missing_controls: list[str]
    overdue_review: bool
    missing_human_oversight: bool
    data_safeguard_issue: bool
    priority_issue: str | None


def load_yaml(path: Path) -> dict[str, Any]:
    """Load a YAML file and return a mapping."""

    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise RegisterValidationError(f"{path.name} must contain a mapping.")
    return data


def load_schema(path: Path) -> dict[str, Any]:
    """Load the local JSON schema metadata."""

    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise RegisterValidationError("schema.json must contain a mapping.")
    return data


def required_fields(schema: dict[str, Any]) -> list[str]:
    """Return required system fields from the schema."""

    return list(schema["properties"]["systems"]["items"]["required"])


def enum_values(schema: dict[str, Any], field: str) -> set[str]:
    """Return allowed enum values for a schema field."""

    properties = schema["properties"]["systems"]["items"]["properties"]
    return set(properties[field]["enum"])


def systems_from_data(data: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract system records from the YAML payload."""

    systems = data.get("systems")
    if not isinstance(systems, list):
        raise RegisterValidationError("systems.yaml must contain a systems list.")
    if not systems:
        raise RegisterValidationError("systems.yaml must contain at least one system.")
    if not all(isinstance(system, dict) for system in systems):
        raise RegisterValidationError("Each system entry must be a mapping.")
    return systems


def validate_required_fields(systems: list[dict[str, Any]], schema: dict[str, Any]) -> None:
    """Validate that every required field is present and populated."""

    fields = required_fields(schema)
    for index, system in enumerate(systems, start=1):
        missing = [field for field in fields if field not in system]
        empty = [
            field
            for field in fields
            if field in system and system[field] in ("", None)
        ]
        if missing or empty:
            system_id = system.get("id", f"entry {index}")
            problems = ", ".join(missing + empty)
            raise RegisterValidationError(
                f"{system_id} is missing required field(s): {problems}"
            )


def validate_enums(systems: list[dict[str, Any]], schema: dict[str, Any]) -> None:
    """Validate allowed values for approved-use status and priority."""

    approved_values = enum_values(schema, "approved_use_status")
    priority_values = enum_values(schema, "governance_priority")
    for system in systems:
        if system["approved_use_status"] not in approved_values:
            raise RegisterValidationError(
                f"{system['id']} has invalid approved_use_status: "
                f"{system['approved_use_status']}"
            )
        if system["governance_priority"] not in priority_values:
            raise RegisterValidationError(
                f"{system['id']} has invalid governance_priority: "
                f"{system['governance_priority']}"
            )


def detect_duplicate_ids(systems: list[dict[str, Any]]) -> None:
    """Raise when two systems use the same ID."""

    seen: set[str] = set()
    duplicates: set[str] = set()
    for system in systems:
        system_id = system["id"]
        if system_id in seen:
            duplicates.add(system_id)
        seen.add(system_id)
    if duplicates:
        raise RegisterValidationError(
            "Duplicate system id(s): " + ", ".join(sorted(duplicates))
        )


def validate_control_ids(systems: list[dict[str, Any]]) -> None:
    """Validate that all declared controls use known control IDs."""

    for system in systems:
        controls = set(system.get("applicable_controls", []))
        unknown = sorted(controls - CONTROL_IDS)
        if unknown:
            raise RegisterValidationError(
                f"{system['id']} has unknown control id(s): {', '.join(unknown)}"
            )


def validate_all(systems: list[dict[str, Any]], schema: dict[str, Any]) -> None:
    """Run all input validations."""

    validate_required_fields(systems, schema)
    validate_enums(systems, schema)
    detect_duplicate_ids(systems)
    validate_control_ids(systems)


def has_public_or_external_users(system: dict[str, Any]) -> bool:
    """Return true when users or affected groups indicate public exposure."""

    combined = " ".join(system["target_users"] + system["affected_groups"]).lower()
    markers = ["resident", "citizen", "visitor", "public", "vulnerable"]
    return any(marker in combined for marker in markers)


def has_automated_decision_impact(system: dict[str, Any]) -> bool:
    """Return true when the system could affect decisions."""

    text = system["automated_decision_impact"].strip().lower()
    return not text.startswith("none")


def calculate_governance_priority(system: dict[str, Any]) -> str:
    """Calculate minimum governance priority using transparent demo rules."""

    if system["approved_use_status"] == "Not approved":
        return "Critical"
    if has_automated_decision_impact(system):
        return "Critical"
    if system["special_category_data"]:
        return "High"
    if system["confidential_information"] and system["personal_data"]:
        return "High"
    if system["personal_data"] or has_public_or_external_users(system):
        return "Medium"
    if system["confidential_information"]:
        return "Medium"
    return "Low"


def required_controls_for(system: dict[str, Any], calculated_priority: str) -> set[str]:
    """Return controls expected for the system under demo rules."""

    controls = {"GOV-01", "GOV-02", "GOV-03", "DAT-01", "HUM-01", "HUM-02", "HUM-03", "AUD-01"}
    if system["personal_data"] or system["special_category_data"] or system["confidential_information"]:
        controls.update({"DAT-02", "DAT-03"})
    if system["source_requirements"].strip().lower() not in {"none", "not required"}:
        controls.add("AUD-02")
    if len(system["languages"]) > 1 or "language" in system["purpose"].lower():
        controls.update({"LNG-01", "LNG-02"})
    if "external" in system["provider_type"].lower() or "vendor" in system["provider_type"].lower():
        controls.update({"VEN-01", "VEN-02"})
    if calculated_priority in {"Medium", "High", "Critical"} or system["lifecycle_status"].lower() == "pre-pilot":
        controls.add("EVA-01")
    return controls


def missing_control_ids(system: dict[str, Any], calculated_priority: str) -> list[str]:
    """Identify required controls not declared as applicable."""

    declared = set(system["applicable_controls"])
    missing = required_controls_for(system, calculated_priority) - declared
    if is_missing_human_oversight(system):
        missing.update({"HUM-01", "HUM-02", "HUM-03"})
    return sorted(missing)


def parse_date(value: str | date, field_name: str, system_id: str) -> date:
    """Parse an ISO date from system data."""

    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise RegisterValidationError(
            f"{system_id} has invalid {field_name}: {value}"
        ) from exc


def is_overdue_review(system: dict[str, Any], reference_date: date = REFERENCE_DATE) -> bool:
    """Return true when next review date is before the fixed reference date."""

    next_review = parse_date(system["next_review_date"], "next_review_date", system["id"])
    return next_review < reference_date


def is_missing_human_oversight(system: dict[str, Any]) -> bool:
    """Return true when review or approval authority is not defined."""

    human_review = system["human_review"].strip().lower()
    approver = system["authorised_approver"].strip().lower()
    no_review_markers = ["none", "no approved", "not defined", "missing"]
    no_approver_markers = ["none", "none assigned", "not assigned", "missing"]
    return any(marker in human_review for marker in no_review_markers) or any(
        marker in approver for marker in no_approver_markers
    )


def has_data_safeguard_issue(system: dict[str, Any], missing_controls: list[str]) -> bool:
    """Flag personal or special-category data without adequate safeguards."""

    if not (system["personal_data"] or system["special_category_data"]):
        return False
    safeguard_controls = {"DAT-01", "DAT-02", "DAT-03", "HUM-01", "HUM-02", "HUM-03", "AUD-01"}
    if system["special_category_data"]:
        safeguard_controls.add("AUD-02")
    declared = set(system["applicable_controls"])
    return bool((safeguard_controls - declared) or set(missing_controls) & safeguard_controls)


def priority_issue(system: dict[str, Any], calculated_priority: str) -> str | None:
    """Return a message when declared priority is below the calculated level."""

    declared = system["governance_priority"]
    if PRIORITY_ORDER[declared] < PRIORITY_ORDER[calculated_priority]:
        return f"Declared {declared}, calculated minimum {calculated_priority}"
    return None


def analyse_system(system: dict[str, Any]) -> SystemAnalysis:
    """Compute governance observations for one system."""

    calculated = calculate_governance_priority(system)
    gaps = missing_control_ids(system, calculated)
    return SystemAnalysis(
        system=system,
        calculated_priority=calculated,
        missing_controls=gaps,
        overdue_review=is_overdue_review(system),
        missing_human_oversight=is_missing_human_oversight(system),
        data_safeguard_issue=has_data_safeguard_issue(system, gaps),
        priority_issue=priority_issue(system, calculated),
    )


def analyse_systems(systems: list[dict[str, Any]]) -> list[SystemAnalysis]:
    """Compute governance observations for all systems."""

    return [analyse_system(system) for system in systems]


def count_by(analyses: list[SystemAnalysis], field: str) -> Counter[str]:
    """Count systems by a direct system field."""

    return Counter(analysis.system[field] for analysis in analyses)


def bullet_list(items: list[str]) -> str:
    """Render a stable Markdown bullet list."""

    return "\n".join(f"- {item}" for item in items) if items else "- None"


def count_table(counter: Counter[str], ordered_values: list[str]) -> str:
    """Render a two-column Markdown count table."""

    lines = ["| Label | Count |", "| --- | ---: |"]
    lines.extend(f"| {label} | {counter.get(label, 0)} |" for label in ordered_values)
    return "\n".join(lines)


def render_control_gap_summary(analyses: list[SystemAnalysis]) -> str:
    """Render portfolio-level control gaps."""

    lines = ["| System | Missing controls |", "| --- | --- |"]
    for analysis in analyses:
        gaps = ", ".join(analysis.missing_controls) if analysis.missing_controls else "None"
        lines.append(f"| {analysis.system['system_name']} | {gaps} |")
    return "\n".join(lines)


def render_overdue_summary(analyses: list[SystemAnalysis]) -> str:
    """Render review timing summary."""

    overdue = [analysis for analysis in analyses if analysis.overdue_review]
    if not overdue:
        return "No systems have overdue review dates."
    lines = ["| System | Next review date | Monitoring owner |", "| --- | --- | --- |"]
    for analysis in overdue:
        system = analysis.system
        lines.append(
            f"| {system['system_name']} | {system['next_review_date']} | {system['monitoring_owner']} |"
        )
    return "\n".join(lines)


def render_system_section(analysis: SystemAnalysis) -> str:
    """Render one detailed system section."""

    system = analysis.system
    missing = ", ".join(analysis.missing_controls) if analysis.missing_controls else "None"
    flags = []
    if analysis.overdue_review:
        flags.append("Overdue lifecycle review")
    if analysis.missing_human_oversight:
        flags.append("Missing human oversight")
    if analysis.data_safeguard_issue:
        flags.append("Personal or special-category data safeguard issue")
    if analysis.priority_issue:
        flags.append(analysis.priority_issue)

    return "\n".join(
        [
            f"## {system['system_name']}",
            "",
            f"- System ID: `{system['id']}`",
            f"- Service area: {system['service_area']}",
            f"- Business owner: {system['business_owner']}",
            f"- Purpose: {system['purpose']}",
            f"- Workflow: {system['workflow']}",
            f"- Approved-use status: {system['approved_use_status']}",
            f"- Declared governance priority: {system['governance_priority']}",
            f"- Calculated governance priority: {analysis.calculated_priority}",
            f"- Lifecycle status: {system['lifecycle_status']}",
            f"- Target users: {', '.join(system['target_users'])}",
            f"- Affected groups: {', '.join(system['affected_groups'])}",
            f"- Languages: {', '.join(system['languages'])}",
            f"- Document types: {', '.join(system['document_types'])}",
            f"- Data categories: {', '.join(system['data_categories'])}",
            f"- Personal data: {system['personal_data']}",
            f"- Special-category data: {system['special_category_data']}",
            f"- Confidential information: {system['confidential_information']}",
            f"- Provider type: {system['provider_type']}",
            f"- Processing location: {system['processing_location']}",
            f"- Approved tools: {', '.join(system['approved_tools']) if system['approved_tools'] else 'None'}",
            f"- Source requirements: {system['source_requirements']}",
            f"- Human-review requirement: {system['human_review']}",
            f"- Authorised approver: {system['authorised_approver']}",
            f"- Automated decision impact: {system['automated_decision_impact']}",
            f"- DPIA review: {system['dpia_review']}",
            f"- Procurement status: {system['procurement_status']}",
            f"- Applicable control IDs: {', '.join(system['applicable_controls'])}",
            f"- Missing control IDs: {missing}",
            f"- Review frequency: {system['review_frequency']}",
            f"- Last review date: {system['last_review_date']}",
            f"- Next review date: {system['next_review_date']}",
            f"- Monitoring owner: {system['monitoring_owner']}",
            f"- Governance flags: {', '.join(flags) if flags else 'None'}",
            "",
            f"Risk note: {system['risk_note']}",
            "",
            "Limitations:",
            bullet_list(system["known_limitations"]),
            "",
            "Mitigations:",
            bullet_list(system["mitigation_measures"]),
        ]
    )


def render_report(analyses: list[SystemAnalysis], reference_date: date = REFERENCE_DATE) -> str:
    """Render the full Markdown exposure register."""

    priority_counts = count_by(analyses, "governance_priority")
    status_counts = count_by(analyses, "approved_use_status")
    gap_count = sum(1 for analysis in analyses if analysis.missing_controls)
    overdue_count = sum(1 for analysis in analyses if analysis.overdue_review)
    safeguard_count = sum(1 for analysis in analyses if analysis.data_safeguard_issue)
    sections = "\n\n".join(render_system_section(analysis) for analysis in analyses)

    return "\n".join(
        [
            "# AI and Language Exposure Register",
            "",
            f"Reference date: {reference_date.isoformat()}",
            "",
            "## Executive Summary",
            "",
            (
                f"This deterministic demo register covers {len(analyses)} fictional municipal systems. "
                f"It identifies {gap_count} system(s) with control gaps, {overdue_count} overdue review(s), "
                f"and {safeguard_count} personal or special-category data safeguard issue(s)."
            ),
            "",
            "The register supports early portfolio visibility before a pilot, procurement process or broader implementation. It is based on the ClearNord governance framework principles of accountable ownership, source-grounded operation, controlled multilingual quality, risk-based use, auditability and vendor readiness.",
            "",
            "## Portfolio Overview",
            "",
            "| System | Service area | Approved-use status | Governance priority | Next review |",
            "| --- | --- | --- | --- | --- |",
            *[
                f"| {analysis.system['system_name']} | {analysis.system['service_area']} | "
                f"{analysis.system['approved_use_status']} | {analysis.system['governance_priority']} | "
                f"{analysis.system['next_review_date']} |"
                for analysis in analyses
            ],
            "",
            "## Counts by Governance Priority",
            "",
            count_table(priority_counts, ["Low", "Medium", "High", "Critical"]),
            "",
            "## Counts by Approved-Use Status",
            "",
            count_table(
                status_counts,
                ["Approved", "Approved with conditions", "Restricted", "Not approved"],
            ),
            "",
            "## Control-Gap Summary",
            "",
            render_control_gap_summary(analyses),
            "",
            "## Overdue-Review Summary",
            "",
            render_overdue_summary(analyses),
            "",
            sections,
            "",
            "## Disclaimer",
            "",
            "This is a deterministic public demonstration using fictional municipal examples. It is not a production system, legal assessment, compliance certification, DPIA, procurement recommendation or final AI Act classification. Internal labels such as Low, Medium, High, Critical, Approved, Approved with conditions, Restricted and Not approved are demo governance labels only.",
            "",
        ]
    )


def generate_register() -> str:
    """Validate input data, generate the report and write it to disk."""

    schema = load_schema(SCHEMA_PATH)
    data = load_yaml(SYSTEMS_PATH)
    systems = systems_from_data(data)
    validate_all(systems, schema)
    analyses = analyse_systems(systems)
    report = render_report(analyses)
    OUTPUT_PATH.write_text(report, encoding="utf-8")
    return report


def main() -> None:
    """CLI entry point."""

    generate_register()
    print(f"Wrote {OUTPUT_PATH.relative_to(Path.cwd())}")


if __name__ == "__main__":
    main()
