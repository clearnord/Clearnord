# ClearNord Governance Demo Suite Report

## Suite Summary

- Suite run ID: `CN-GOVERNANCE-SUITE-2026-07-01`
- Framework path: `frameworks/public-sector-ai-language-governance.md`
- Generators succeeded: 5 of 5
- Test status: Succeeded

## Demos

| Demo | Directory | Generated report | Generator status |
| --- | --- | --- | --- |
| AI and language exposure register | `demos/ai-language-exposure-register` | `demos/ai-language-exposure-register/EXPOSURE_REGISTER.md` | Succeeded |
| Norwegian language controls | `demos/norwegian-language-controls` | `demos/norwegian-language-controls/LANGUAGE_CONTROL_REPORT.md` | Succeeded |
| Vendor readiness scorecard | `demos/vendor-readiness-scorecard` | `demos/vendor-readiness-scorecard/VENDOR_SCORECARD.md` | Succeeded |
| Grounded answer transparency | `demos/grounded-answer-transparency` | `demos/grounded-answer-transparency/ANSWER_LOG.md` | Succeeded |
| Red-team evaluation kit | `demos/red-team-evaluation-kit` | `demos/red-team-evaluation-kit/EVALUATION_REPORT.md` | Succeeded |

## Generator Details

### AI and language exposure register

- Command: `python demos/ai-language-exposure-register/generate_register.py`
- Status: Succeeded
- Return code: 0
- Output: Wrote demos/ai-language-exposure-register/EXPOSURE_REGISTER.md

### Norwegian language controls

- Command: `python demos/norwegian-language-controls/run_language_checks.py`
- Status: Succeeded
- Return code: 0
- Output: Wrote demos/norwegian-language-controls/LANGUAGE_CONTROL_REPORT.md
Checked 4 documents with 21 finding(s)

### Vendor readiness scorecard

- Command: `python demos/vendor-readiness-scorecard/score_vendor.py`
- Status: Succeeded
- Return code: 0
- Output: Wrote demos/vendor-readiness-scorecard/VENDOR_SCORECARD.md
Result: Yellow: clarification or compensating controls required before pilot
Weighted score: 71.1

### Grounded answer transparency

- Command: `python demos/grounded-answer-transparency/run_grounding_demo.py`
- Status: Succeeded
- Return code: 0
- Output: Wrote demos/grounded-answer-transparency/ANSWER_LOG.md
Outcome counts: Answered from approved source=2, Escalated for human review=1, Refused: insufficient source support=1, Refused: no approved source=1

### Red-team evaluation kit

- Command: `python demos/red-team-evaluation-kit/run_evaluations.py`
- Status: Succeeded
- Return code: 0
- Output: Wrote demos/red-team-evaluation-kit/EVALUATION_REPORT.md
Release recommendation: Release blocked
Pass rate: 68.8%

## Test Summary

- Command: `python -m pytest demos/ai-language-exposure-register/tests demos/norwegian-language-controls/tests demos/vendor-readiness-scorecard/tests demos/grounded-answer-transparency/tests demos/red-team-evaluation-kit/tests --basetemp=.pytest_cache/basetemp -q`
- Status: Succeeded
- Return code: 0
- Output: .............................................                            [100%]
45 passed in 0.44s

## Deterministic Execution Statement

The suite uses fixed run identifiers and deterministic inputs. It does not use current timestamps, network calls, external APIs or real model calls.

## Data-Handling Statement

All examples are fictional. The suite does not contain real personal data, real municipality data, real vendor assessments or secrets.

## Limitations

- The reports support early governance and assurance discussion only.
- The demos use deterministic rules and mock examples, not production systems.
- Human review remains necessary for rights-affecting, procurement, security, language-quality and publication decisions.
- The red-team kit intentionally includes failing mock responses to demonstrate failure detection.

## Disclaimer

This deterministic demonstration supports early governance and assurance
work. It does not provide legal advice, compliance certification, a final
procurement decision, a DPIA, a security approval or a production-readiness
determination.
