# Vendor Readiness Scorecard Demo

This deterministic demo shows how ClearNord could structure an early public-sector AI vendor assessment before a controlled pilot, procurement decision or contractual review.

It reuses the ClearNord governance framework themes of vendor and procurement readiness, human accountability, auditability, source-grounded operation, controlled multilingual quality and risk-based use. The scorecard is intentionally evidence-oriented: a good answer is weaker when the supporting evidence is only a vendor statement.

This deterministic demonstration supports early governance and assurance
work. It does not provide legal advice, compliance certification, a final
procurement decision, a DPIA, a security approval or a production-readiness
determination.

## What It Checks

The questionnaire covers processing location, customer-data training, retention, deletion, logging, audit export, human oversight, explainability, DPIA support, security documentation, access control, subprocessors, incidents, accessibility, Bokmal and Nynorsk support, terminology testing, exportability, exit planning, lock-in, retention configuration, material model-change notices and evidence quality.

## How To Run

```bash
python demos/vendor-readiness-scorecard/score_vendor.py
python -m pytest demos/vendor-readiness-scorecard/tests -q
```

PyYAML is the only runtime dependency. Pytest is used for tests.

## How To Interpret The Report

Traffic-light outcomes are deterministic:

- Green: acceptable for a controlled pilot, subject to ordinary approvals
- Yellow: clarification or compensating controls required before pilot
- Red: not ready for public-sector pilot

Hard stops override score. For example, shared-model training with customer data or unavailable current security documentation produces Red even if the weighted score is otherwise high.

## Human Review

Procurement, legal, security, data protection, language-quality and service owners must review the evidence before any pilot or contractual decision. This demo only organises early questions and gaps.
