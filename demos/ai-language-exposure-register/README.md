# AI and Language Exposure Register Demo

## What this demo demonstrates

This deterministic demo shows how ClearNord could document AI and language-tool exposure across a small municipal portfolio before a pilot, procurement process or broader implementation.

The register turns structured system information into a stable Markdown report with:

- portfolio-level governance priority counts
- approved-use status counts
- control gaps
- overdue review signals
- human-review and approval requirements
- data and source-grounding concerns
- one detailed section per mock municipal system

The demo uses the governance principles, workflow stages, risk levels, stop conditions and documentation requirements from the ClearNord public-sector AI and language governance framework.

## Relation to AI and language exposure analysis

AI and language exposure analysis is an early governance activity. It helps a municipality understand where language technology is being considered, what data and groups may be affected, which controls are already present, and what must be resolved before a tool is piloted or procured.

This demo focuses on exposure visibility rather than technical model evaluation. It supports questions such as:

- Which systems involve personal data or sensitive service contexts?
- Which systems need stronger human review before use?
- Which systems have overdue lifecycle review dates?
- Which governance controls are missing?
- Which use cases should remain restricted until safeguards are documented?

## What this demo does not claim

This is not a production system, legal assessment, compliance certification, DPIA, procurement recommendation or final AI Act classification. The labels in the generated report are internal demo governance labels only.

The examples are fictional and do not name any real municipality, citizen, employee or vendor.

## How to run it

Install the runtime dependency and test dependency in your preferred Python 3.11+ environment:

```bash
python -m pip install PyYAML pytest
```

Generate the exposure register:

```bash
python demos/ai-language-exposure-register/generate_register.py
```

Run tests:

```bash
python -m pytest demos/ai-language-exposure-register/tests -q
```

## Files

- `systems.yaml`: four fictional municipal AI and language-tool examples
- `schema.json`: required fields and allowed enum values
- `risk_matrix.md`: demo risk and approval label definitions
- `control_mapping.md`: transparent governance control IDs
- `generate_register.py`: deterministic report generator
- `EXPOSURE_REGISTER.md`: generated Markdown report
- `tests/test_register.py`: pytest coverage for validation and reporting behavior

## Why this is useful to a municipality

A municipality can use this style of register to prepare for decisions before a pilot, procurement or service rollout. It gives legal, procurement, service, language and technology owners a shared view of proposed tools, affected groups, required safeguards and unresolved control gaps.

The output is intentionally simple Markdown so it can be reviewed in ordinary governance meetings, archived with procurement material, and updated as controls mature.
