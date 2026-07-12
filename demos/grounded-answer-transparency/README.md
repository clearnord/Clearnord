# Grounded Answer Transparency Demo

This deterministic demo shows the ClearNord principle that public-sector AI should not produce unsupported answers. It uses approved fictional source texts, simple deterministic matching and predefined answer templates. It does not call an LLM or any external API.

This deterministic demonstration supports early governance and assurance
work. It does not provide legal advice, compliance certification, a final
procurement decision, a DPIA, a security approval or a production-readiness
determination.

## What It Demonstrates

The demo separates topical relevance from sufficient evidence. A source can be related to a question without supporting the specific answer. When evidence is insufficient, the system refuses or escalates rather than inventing a processing time, right, entitlement or decision.

## How To Run

```bash
python demos/grounded-answer-transparency/run_grounding_demo.py
python -m pytest demos/grounded-answer-transparency/tests -q
```

PyYAML is the only runtime dependency. Pytest is used for tests.

## How To Interpret The Report

`ANSWER_LOG.md` records each question, outcome, matched evidence, support assessment, confidence, limitations, human-review requirement, control IDs and the fixed audit run ID.

Outcomes are:

- Answered from approved source
- Refused: no approved source
- Refused: insufficient source support
- Escalated for human review

## Human Review

Human review remains necessary where a question affects rights, duties, deadlines, personal data, service access or any case-specific decision. The demo is an assurance pattern, not a service tool.
