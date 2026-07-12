# Grounded Answer Transparency Log

## Executive Summary

Audit run ID: CN-GROUNDING-DEMO-2026-07-01

Questions checked: 5

This log demonstrates deterministic refusal when approved sources do not support a specific answer.

## Counts By Outcome

| Outcome | Count |
| --- | ---: |
| Answered from approved source | 2 |
| Escalated for human review | 1 |
| Refused: insufficient source support | 1 |
| Refused: no approved source | 1 |

## q1-service-hours

- Question: When is the service centre open?
- Outcome: Answered from approved source
- Answer or refusal: The service centre is open Monday to Friday from 09:00 to 15:00.
- Approved sources: service-centre-contact
- Matched evidence: centre, open, service
- Support assessment: 3 matched term(s); threshold 2
- Confidence: 0.8
- Limitations: Topical relevance is not enough; the specific answer must be supported by approved text.
- Human-review requirement: False
- Control IDs: RAG-01, RAG-02, RAG-03, AUD-02, HUM-01
- Audit run ID: CN-GROUNDING-DEMO-2026-07-01

## q2-secure-documents

- Question: Can I send documents with personal information by ordinary email?
- Outcome: Answered from approved source
- Answer or refusal: No. Documents containing personal information should be submitted through the secure document portal, not ordinary email.
- Approved sources: secure-document-submission
- Matched evidence: documents, email, information, ordinary, personal, send
- Support assessment: 6 matched term(s); threshold 2
- Confidence: 0.95
- Limitations: Topical relevance is not enough; the specific answer must be supported by approved text.
- Human-review requirement: False
- Control IDs: RAG-01, RAG-02, RAG-03, AUD-02, HUM-01
- Audit run ID: CN-GROUNDING-DEMO-2026-07-01

## q3-appeal-guidance

- Question: Can the AI tell me whether my appeal will succeed?
- Outcome: Escalated for human review
- Answer or refusal: Automated tools must not decide whether an appeal will succeed. General appeal information is normally found in the written decision letter.
- Approved sources: appeal-guidance
- Matched evidence: appeal, succeed, whether, will
- Support assessment: 4 matched term(s); threshold 2
- Confidence: 0.9
- Limitations: Topical relevance is not enough; the specific answer must be supported by approved text.
- Human-review requirement: True
- Control IDs: RAG-01, RAG-02, RAG-03, AUD-02, HUM-01
- Audit run ID: CN-GROUNDING-DEMO-2026-07-01

## q4-building-processing-time

- Question: What is the current building-case processing time?
- Outcome: Refused: no approved source
- Answer or refusal: No approved source covers this topic.
- Approved sources: None
- Matched evidence: None
- Support assessment: 0 matched term(s); threshold 2
- Confidence: 0.0
- Limitations: Topical relevance is not enough; the specific answer must be supported by approved text.
- Human-review requirement: True
- Control IDs: RAG-01, RAG-02, RAG-03, AUD-02, HUM-01
- Audit run ID: CN-GROUNDING-DEMO-2026-07-01

## q5-specific-appeal-deadline

- Question: What exact appeal deadline applies to my individual case?
- Outcome: Refused: insufficient source support
- Answer or refusal: The related source does not support a precise answer to this question.
- Approved sources: appeal-guidance
- Matched evidence: appeal, individual
- Support assessment: 2 matched term(s); threshold 5
- Confidence: 0.4
- Limitations: Topical relevance is not enough; the specific answer must be supported by approved text.
- Human-review requirement: True
- Control IDs: RAG-01, RAG-02, RAG-03, AUD-02, HUM-01
- Audit run ID: CN-GROUNDING-DEMO-2026-07-01

## Disclaimer

This deterministic demonstration supports early governance and assurance
work. It does not provide legal advice, compliance certification, a final
procurement decision, a DPIA, a security approval or a production-readiness
determination.
