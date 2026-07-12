"""Run the deterministic ClearNord governance demo suite."""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


SUITE_RUN_ID = "CN-GOVERNANCE-SUITE-2026-07-01"
FRAMEWORK_PATH = Path("frameworks/public-sector-ai-language-governance.md")
REPORT_PATH = Path("SUITE_REPORT.md")
DISCLAIMER = (
    "This deterministic demonstration supports early governance and assurance\n"
    "work. It does not provide legal advice, compliance certification, a final\n"
    "procurement decision, a DPIA, a security approval or a production-readiness\n"
    "determination."
)


@dataclass(frozen=True)
class Demo:
    """One deterministic demo generator in the suite."""

    name: str
    directory: Path
    generator: Path
    report: Path


@dataclass(frozen=True)
class CommandResult:
    """Stable command execution result for reporting."""

    label: str
    command: list[str]
    returncode: int
    output: str

    @property
    def status(self) -> str:
        """Return a human-readable command status."""

        return "Succeeded" if self.returncode == 0 else "Failed"


DEMOS = [
    Demo(
        "AI and language exposure register",
        Path("demos/ai-language-exposure-register"),
        Path("demos/ai-language-exposure-register/generate_register.py"),
        Path("demos/ai-language-exposure-register/EXPOSURE_REGISTER.md"),
    ),
    Demo(
        "Norwegian language controls",
        Path("demos/norwegian-language-controls"),
        Path("demos/norwegian-language-controls/run_language_checks.py"),
        Path("demos/norwegian-language-controls/LANGUAGE_CONTROL_REPORT.md"),
    ),
    Demo(
        "Vendor readiness scorecard",
        Path("demos/vendor-readiness-scorecard"),
        Path("demos/vendor-readiness-scorecard/score_vendor.py"),
        Path("demos/vendor-readiness-scorecard/VENDOR_SCORECARD.md"),
    ),
    Demo(
        "Grounded answer transparency",
        Path("demos/grounded-answer-transparency"),
        Path("demos/grounded-answer-transparency/run_grounding_demo.py"),
        Path("demos/grounded-answer-transparency/ANSWER_LOG.md"),
    ),
    Demo(
        "Red-team evaluation kit",
        Path("demos/red-team-evaluation-kit"),
        Path("demos/red-team-evaluation-kit/run_evaluations.py"),
        Path("demos/red-team-evaluation-kit/EVALUATION_REPORT.md"),
    ),
]

TEST_COMMAND = [
    sys.executable,
    "-m",
    "pytest",
    "demos/ai-language-exposure-register/tests",
    "demos/norwegian-language-controls/tests",
    "demos/vendor-readiness-scorecard/tests",
    "demos/grounded-answer-transparency/tests",
    "demos/red-team-evaluation-kit/tests",
    "--basetemp=.pytest_cache/basetemp",
    "-q",
]


def run_command(label: str, command: list[str], display_command: list[str] | None = None) -> CommandResult:
    """Run a local command without shell expansion or network access."""

    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )
    output = "\n".join(part.strip() for part in (completed.stdout, completed.stderr) if part.strip())
    output = output.replace("\\", "/")
    return CommandResult(
        label=label,
        command=display_command or command,
        returncode=completed.returncode,
        output=output,
    )


def run_generators() -> list[CommandResult]:
    """Run all demo generators in stable order."""

    return [
        run_command(
            demo.name,
            [sys.executable, str(demo.generator)],
            ["python", demo.generator.as_posix()],
        )
        for demo in DEMOS
    ]


def run_tests() -> CommandResult:
    """Run the full deterministic demo test suite."""

    return run_command("pytest", TEST_COMMAND, ["python", *TEST_COMMAND[1:]])


def bullet_list(items: list[str]) -> list[str]:
    """Render a Markdown bullet list, with a fallback empty marker."""

    return [f"- {item}" for item in items] if items else ["- None"]


def render_report(generator_results: list[CommandResult], test_result: CommandResult) -> str:
    """Render the deterministic suite report."""

    generator_by_name = {result.label: result for result in generator_results}
    failed_generators = [result.label for result in generator_results if result.returncode != 0]
    lines = [
        "# ClearNord Governance Demo Suite Report",
        "",
        "## Suite Summary",
        "",
        f"- Suite run ID: `{SUITE_RUN_ID}`",
        f"- Framework path: `{FRAMEWORK_PATH.as_posix()}`",
        f"- Generators succeeded: {len(generator_results) - len(failed_generators)} of {len(generator_results)}",
        f"- Test status: {test_result.status}",
        "",
        "## Demos",
        "",
        "| Demo | Directory | Generated report | Generator status |",
        "| --- | --- | --- | --- |",
    ]
    for demo in DEMOS:
        result = generator_by_name[demo.name]
        lines.append(
            f"| {demo.name} | `{demo.directory.as_posix()}` | `{demo.report.as_posix()}` | {result.status} |"
        )
    lines.extend(
        [
            "",
            "## Generator Details",
            "",
        ]
    )
    for result in generator_results:
        lines.extend(
            [
                f"### {result.label}",
                "",
                f"- Command: `{' '.join(result.command)}`",
                f"- Status: {result.status}",
                f"- Return code: {result.returncode}",
                f"- Output: {result.output or 'No output'}",
                "",
            ]
        )
    lines.extend(
        [
            "## Test Summary",
            "",
            f"- Command: `{' '.join(test_result.command)}`",
            f"- Status: {test_result.status}",
            f"- Return code: {test_result.returncode}",
            f"- Output: {test_result.output or 'No output'}",
            "",
            "## Deterministic Execution Statement",
            "",
            "The suite uses fixed run identifiers and deterministic inputs. It does not use current timestamps, network calls, external APIs or real model calls.",
            "",
            "## Data-Handling Statement",
            "",
            "All examples are fictional. The suite does not contain real personal data, real municipality data, real vendor assessments or secrets.",
            "",
            "## Limitations",
            "",
            *bullet_list(
                [
                    "The reports support early governance and assurance discussion only.",
                    "The demos use deterministic rules and mock examples, not production systems.",
                    "Human review remains necessary for rights-affecting, procurement, security, language-quality and publication decisions.",
                    "The red-team kit intentionally includes failing mock responses to demonstrate failure detection.",
                ]
            ),
            "",
            "## Disclaimer",
            "",
            DISCLAIMER,
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    """Run generators, run tests, write the suite report and return status."""

    generator_results = run_generators()
    test_result = run_tests()
    REPORT_PATH.write_text(render_report(generator_results, test_result), encoding="utf-8")
    if any(result.returncode != 0 for result in generator_results):
        return 1
    if test_result.returncode != 0:
        return test_result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
