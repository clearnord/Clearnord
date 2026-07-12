# Norwegian Public-Sector Language Controls Demo

## What this demo demonstrates

This deterministic demo shows early-warning controls for Norwegian public-sector and citizen-facing text. It treats language quality as part of AI governance because unclear wording, mixed language standards, hidden internal notes and weak responsibility signals can affect public trust, accessibility, accountability and publication readiness.

The demo checks four fictional Markdown documents with YAML front matter. It produces a stable report that can support human review before text is published, reused in an AI-assisted workflow or included in a controlled multilingual communication process.

## Why language quality is part of AI governance

The ClearNord governance framework requires human accountability, controlled multilingual quality, auditability and review before external use. Language technology can make text faster to draft or transform, but it can also carry forward internal notes, obscure responsibility, mix written standards or make next steps unclear.

These controls help teams identify issues that should be resolved by content owners, language reviewers or subject-matter reviewers before publication.

## Norwegian public-sector communication

Norwegian public-sector text must often serve residents with different language needs, service contexts and levels of administrative knowledge. A deterministic early-warning pass can help detect governance-relevant conditions such as unclear audience, inconsistent naming, vague timing and missing next steps.

The examples are fictional. They do not name any real municipality, citizen, employee, vendor or individual case.

## Early-warning limitation

These are deterministic early-warning checks. The report does not determine legal compliance, final linguistic correctness or whether a publication is suitable for a specific audience.

Keyword and metadata checks can identify review needs, but they cannot decide whether a text is legally sufficient, linguistically correct in every context, aligned with Språklova, aligned with accessibility law or suitable for all readers.

## How to run it

Install the runtime dependency and test dependency in a Python 3.11+ environment:

```bash
python -m pip install PyYAML pytest
```

Generate the report:

```bash
python demos/norwegian-language-controls/run_language_checks.py
```

Run tests:

```bash
python -m pytest demos/norwegian-language-controls/tests -q
```

## How to interpret the report

The report groups findings by severity, control ID and document. Publication-readiness statuses are deterministic:

- `Revision required before publication`: one or more high findings
- `Human language review required`: no high findings, but at least one medium finding requiring human review
- `Ready for editorial review`: only low or info findings, or no findings

The first example is a clean baseline. It should have no high-severity findings and should show how a small citizen-facing notice can document audience, responsibility, timing and next step.

## When human review is still necessary

Human language or subject-matter review is still necessary when text affects access to services, explains rights or duties, addresses vulnerable users, mixes written standards, contains internal workflow material, or relies on administrative terminology that may confuse residents.

The report is designed to route attention, not replace judgement.
