"""Run the deterministic ClearNord governance demo suite."""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


SUITE_RUN_ID = "CN-GOVERNANCE-SUITE-2026-07-01"
FRAMEWORK_PATH = Path("frameworks/public-sector-ai-language-governance.md")
REPORT_PATH = Path("SUITE_REPORT.md")
EXPOSURE_REGISTER_NEWLINE = "\r\n"
DEFAULT_REPORT_NEWLINE = "\n"
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
    newline: str = DEFAULT_REPORT_NEWLINE


@dataclass(frozen=True)
class CommandResult:
    """Stable command execution result for reporting."""

    label: str
    command: list[str]
    returncode: int
    stdout: str
    stderr: str

    @property
    def status(self) -> str:
        """Return a human-readable command status."""

        return "Succeeded" if self.returncode == 0 else "Failed"

    @property
    def output(self) -> str:
        """Return combined command output for the Markdown report."""

        return "\n".join(part for part in (self.stdout, self.stderr) if part)


DEMOS = [
    Demo(
        "AI and language exposure register",
        Path("demos/ai-language-exposure-register"),
        Path("demos/ai-language-exposure-register/generate_register.py"),
        Path("demos/ai-language-exposure-register/EXPOSURE_REGISTER.md"),
        EXPOSURE_REGISTER_NEWLINE,
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

TEST_COMMAND_DISPLAY = [
    "python",
    "-m",
    "pytest",
    "demos/ai-language-exposure-register/tests",
    "demos/norwegian-language-controls/tests",
    "demos/vendor-readiness-scorecard/tests",
    "demos/grounded-answer-transparency/tests",
    "demos/red-team-evaluation-kit/tests",
    "--basetemp=.pytest-basetemp",
    "-q",
]
TEST_SUMMARY = "Tests are run by `make test` after report generation."


def run_command(label: str, command: list[str], display_command: list[str] | None = None) -> CommandResult:
    """Run a local command without shell expansion or network access."""

    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )
    stdout = completed.stdout.strip().replace("\\", "/")
    stderr = completed.stderr.strip().replace("\\", "/")
    return CommandResult(
        label=label,
        command=display_command or command,
        returncode=completed.returncode,
        stdout=stdout,
        stderr=stderr,
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


def normalise_demo_reports() -> None:
    """Rewrite generated demo reports with stable committed line endings."""

    for demo in DEMOS:
        text = demo.report.read_text(encoding="utf-8")
        demo.report.write_text(text, encoding="utf-8", newline=demo.newline)


def print_failure_details(results: list[CommandResult]) -> None:
    """Print full generator diagnostics when a generator fails."""

    for result in results:
        if result.returncode == 0:
            continue
        print(f"Generator failed: {result.label}", file=sys.stderr)
        print(f"Command: {' '.join(result.command)}", file=sys.stderr)
        print(f"Return code: {result.returncode}", file=sys.stderr)
        print("Stdout:", file=sys.stderr)
        print(result.stdout or "No stdout", file=sys.stderr)
        print("Stderr:", file=sys.stderr)
        print(result.stderr or "No stderr", file=sys.stderr)


def bullet_list(items: list[str]) -> list[str]:
    """Render a Markdown bullet list, with a fallback empty marker."""

    return [f"- {item}" for item in items] if items else ["- None"]


def render_report(generator_results: list[CommandResult]) -> str:
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
        f"- Test status: {TEST_SUMMARY}",
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
            f"- Command: `{' '.join(TEST_COMMAND_DISPLAY)}`",
            f"- Status: {TEST_SUMMARY}",
            "- Return code: Not recorded by `run_all.py`",
            "- Output: See the separate `make test` command or GitHub Actions test step.",
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
    """Run generators, write the suite report and return generator status."""

    generator_results = run_generators()
    if not any(result.returncode != 0 for result in generator_results):
        normalise_demo_reports()
    REPORT_PATH.write_text(render_report(generator_results), encoding="utf-8", newline="\n")
    if any(result.returncode != 0 for result in generator_results):
        print_failure_details(generator_results)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
