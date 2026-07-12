# Red-Team Evaluation Kit Demo

This deterministic demo shows how ClearNord could evaluate an AI-supported public-sector workflow before recommending a pilot or broader use. It uses predefined mock responses only. It does not call a real model, LLM or external API.

This deterministic demonstration supports early governance and assurance
work. It does not provide legal advice, compliance certification, a final
procurement decision, a DPIA, a security approval or a production-readiness
determination.

## What It Demonstrates

The kit checks prompt injection, hidden instruction disclosure, personal-data leakage, special-category data leakage, hallucinated legal advice, unsupported entitlement claims, unsafe automated rejection, missing or unapproved citations, overconfidence, missing limitations, failure to escalate, role-play bypass, unsupported processing-time claims, refusal quality and harmful language transformation.

It intentionally includes failing tests. The purpose is to show that the evaluation process can identify failure, not to create an unrealistic perfect score.

## How To Run

```bash
python demos/red-team-evaluation-kit/run_evaluations.py
python -m pytest demos/red-team-evaluation-kit/tests -q
```

PyYAML is the only runtime dependency. Pytest is used for tests.

## How To Interpret The Report

`EVALUATION_REPORT.md` records pass rate, failure counts, release recommendation, release-blocking failures, remediation and one detailed section per test.

Release recommendations are:

- Continue controlled evaluation
- Remediation required before pilot
- Release blocked

High or critical failing release-blocking cases produce `Release blocked`.

## Human Review

Human review remains necessary for residual risk acceptance, release decisions, public-sector language quality, source traceability and rights-affecting workflows. Automated assertions are only an early assurance layer.
