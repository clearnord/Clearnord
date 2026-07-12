# AI and Language Exposure Register

Reference date: 2026-07-01

## Executive Summary

This deterministic demo register covers 4 fictional municipal systems. It identifies 2 system(s) with control gaps, 1 overdue review(s), and 1 personal or special-category data safeguard issue(s).

The register supports early portfolio visibility before a pilot, procurement process or broader implementation. It is based on the ClearNord governance framework principles of accountable ownership, source-grounded operation, controlled multilingual quality, risk-based use, auditability and vendor readiness.

## Portfolio Overview

| System | Service area | Approved-use status | Governance priority | Next review |
| --- | --- | --- | --- | --- |
| Internal document assistant | Internal administration | Approved with conditions | Medium | 2026-08-15 |
| Citizen-service chatbot | Citizen service and front desk | Approved with conditions | Medium | 2026-07-20 |
| Case-summary assistant | Welfare and individual services | Not approved | Critical | 2026-06-15 |
| Language simplification assistant | Public communication | Approved with conditions | Medium | 2026-09-01 |

## Counts by Governance Priority

| Label | Count |
| --- | ---: |
| Low | 0 |
| Medium | 3 |
| High | 0 |
| Critical | 1 |

## Counts by Approved-Use Status

| Label | Count |
| --- | ---: |
| Approved | 0 |
| Approved with conditions | 3 |
| Restricted | 0 |
| Not approved | 1 |

## Control-Gap Summary

| System | Missing controls |
| --- | --- |
| Internal document assistant | None |
| Citizen-service chatbot | VEN-02 |
| Case-summary assistant | AUD-01, AUD-02, DAT-03, EVA-01, GOV-03, HUM-01, HUM-02, HUM-03, LNG-02, VEN-01, VEN-02 |
| Language simplification assistant | None |

## Overdue-Review Summary

| System | Next review date | Monitoring owner |
| --- | --- | --- |
| Case-summary assistant | 2026-06-15 | Service governance board |

## Internal document assistant

- System ID: `internal-document-assistant`
- Service area: Internal administration
- Business owner: Digital service coordinator, fictional municipality
- Purpose: Support employees with drafting, restructuring and summarising internal policy and meeting material.
- Workflow: Internal drafting support before human review and ordinary document approval.
- Approved-use status: Approved with conditions
- Declared governance priority: Medium
- Calculated governance priority: Medium
- Lifecycle status: Pre-pilot
- Target users: municipal employees, service managers
- Affected groups: municipal employees, internal decision makers
- Languages: Norwegian Bokmal, Norwegian Nynorsk, English
- Document types: meeting notes, internal policy drafts, administrative guidance
- Data categories: internal administrative information, non-sensitive operational notes
- Personal data: False
- Special-category data: False
- Confidential information: True
- Provider type: municipality-managed approved SaaS
- Processing location: EEA-hosted environment with municipal tenant controls
- Approved tools: approved internal language assistant
- Source requirements: Approved internal source documents must be linked in the work item.
- Human-review requirement: Required before internal publication or management use.
- Authorised approver: Unit manager or delegated document owner
- Automated decision impact: None
- DPIA review: Not required for current low-volume internal drafting scope.
- Procurement status: Existing approved internal tool, pilot conditions documented.
- Applicable control IDs: GOV-01, GOV-02, GOV-03, DAT-01, DAT-02, DAT-03, HUM-01, HUM-02, HUM-03, LNG-01, LNG-02, VEN-01, VEN-02, AUD-01, AUD-02, EVA-01
- Missing control IDs: None
- Review frequency: Quarterly during pilot
- Last review date: 2026-05-15
- Next review date: 2026-08-15
- Monitoring owner: Internal governance coordinator
- Governance flags: None

Risk note: Use is limited to drafting support; employees remain responsible for accuracy, tone and source checks.

Limitations:
- May over-summarise nuance in internal discussions.
- Must not be used for employee performance assessments.

Mitigations:
- Require source links for all summaries.
- Keep human approval in the ordinary document workflow.
- Exclude personnel matters from the pilot.

## Citizen-service chatbot

- System ID: `citizen-service-chatbot`
- Service area: Citizen service and front desk
- Business owner: Service desk lead, fictional municipality
- Purpose: Answer common service questions and route citizens to approved municipal information pages.
- Workflow: Public-facing question answering with scripted fallback to human service desk.
- Approved-use status: Approved with conditions
- Declared governance priority: Medium
- Calculated governance priority: Medium
- Lifecycle status: Pre-pilot
- Target users: residents, visitors, service desk employees
- Affected groups: residents seeking municipal services, users with limited Norwegian proficiency, users needing accessible language
- Languages: Norwegian Bokmal, Norwegian Nynorsk, English
- Document types: service descriptions, opening hours, application guidance, contact-routing text
- Data categories: public service information, optional user-provided contact context
- Personal data: True
- Special-category data: False
- Confidential information: False
- Provider type: external managed service without named vendor in demo
- Processing location: EEA processing declared; evidence to be confirmed before pilot expansion
- Approved tools: approved chatbot sandbox, approved municipal knowledge base
- Source requirements: Responses must be grounded in approved public web pages and service desk scripts.
- Human-review requirement: Human handoff required for complex, individual or rights-affecting questions.
- Authorised approver: Head of citizen service
- Automated decision impact: None; chatbot may not decide eligibility, priority or entitlement.
- DPIA review: Screening completed; full DPIA required before processing free-text personal data at scale.
- Procurement status: Pre-procurement market dialogue
- Applicable control IDs: GOV-01, GOV-02, GOV-03, DAT-01, DAT-02, DAT-03, HUM-01, HUM-02, HUM-03, LNG-01, LNG-02, VEN-01, AUD-01, AUD-02, EVA-01
- Missing control IDs: VEN-02
- Review frequency: Monthly during public pilot
- Last review date: 2026-06-10
- Next review date: 2026-07-20
- Monitoring owner: Citizen service quality lead
- Governance flags: None

Risk note: Public-facing language quality and fallback behavior must be monitored closely before broader deployment.

Limitations:
- May misunderstand vague service questions.
- Must not request national identity numbers, health details or case-specific facts.
- Processing-location evidence is not yet complete.

Mitigations:
- Use approved source pages only.
- Display clear no-decision notice.
- Route uncertain or personal questions to human service desk.
- Complete processing-location evidence before extended pilot.

## Case-summary assistant

- System ID: `case-summary-assistant`
- Service area: Welfare and individual services
- Business owner: Casework improvement lead, fictional municipality
- Purpose: Summarise case material for caseworkers before meetings or draft decisions.
- Workflow: Proposed summarisation of individual case records; not approved for operational use.
- Approved-use status: Not approved
- Declared governance priority: Critical
- Calculated governance priority: Critical
- Lifecycle status: Stopped
- Target users: caseworkers, specialist advisers
- Affected groups: residents with individual service cases, vulnerable residents, guardians or family contacts mentioned in case material
- Languages: Norwegian Bokmal, Norwegian Nynorsk
- Document types: case notes, application material, professional assessments, meeting summaries
- Data categories: personal data, special-category data, confidential case information
- Personal data: True
- Special-category data: True
- Confidential information: True
- Provider type: proposed external AI service without completed procurement controls
- Processing location: Not documented
- Approved tools: None
- Source requirements: Source traceability design is not approved.
- Human-review requirement: No approved human review workflow.
- Authorised approver: None assigned
- Automated decision impact: Potential impact if summaries influence rights-affecting case decisions; not approved.
- DPIA review: Required but not completed.
- Procurement status: Not ready for procurement or pilot
- Applicable control IDs: GOV-01, GOV-02, DAT-01, DAT-02, LNG-01
- Missing control IDs: AUD-01, AUD-02, DAT-03, EVA-01, GOV-03, HUM-01, HUM-02, HUM-03, LNG-02, VEN-01, VEN-02
- Review frequency: Before any renewed proposal
- Last review date: 2026-04-01
- Next review date: 2026-06-15
- Monitoring owner: Service governance board
- Governance flags: Overdue lifecycle review, Missing human oversight, Personal or special-category data safeguard issue

Risk note: Stop condition triggered because sensitive case material lacks approved processing route, human oversight and source traceability.

Limitations:
- Cannot verify all facts against approved case sources.
- Missing approved route for special-category data.
- Missing accountable approval and escalation design.

Mitigations:
- Do not pilot with real case data.
- Complete DPIA and procurement controls before any test with operational material.
- Design source traceability and mandatory caseworker review.
- Use synthetic or fully anonymised material for any early demonstration.

## Language simplification assistant

- System ID: `language-simplification-assistant`
- Service area: Public communication
- Business owner: Communications lead, fictional municipality
- Purpose: Simplify approved municipal text so public information is easier to understand.
- Workflow: Language simplification of already-approved public information followed by communications review.
- Approved-use status: Approved with conditions
- Declared governance priority: Medium
- Calculated governance priority: Medium
- Lifecycle status: Pre-pilot
- Target users: communications employees, service-area content owners
- Affected groups: residents reading municipal guidance, residents with limited administrative vocabulary, residents using translated support material
- Languages: Norwegian Bokmal, Norwegian Nynorsk, English, Plain language variant
- Document types: public guidance text, application instructions, service descriptions
- Data categories: public information, non-personal service text
- Personal data: False
- Special-category data: False
- Confidential information: False
- Provider type: municipality-managed approved language tool
- Processing location: EEA-hosted environment with no personal data in prompt
- Approved tools: approved plain-language assistant
- Source requirements: Only approved public source text may be simplified.
- Human-review requirement: Communications review required before publication.
- Authorised approver: Communications editor
- Automated decision impact: None
- DPIA review: Not required for public non-personal text scope.
- Procurement status: Existing approved tool for controlled content work
- Applicable control IDs: GOV-01, GOV-02, GOV-03, DAT-01, DAT-02, DAT-03, HUM-01, HUM-02, HUM-03, LNG-01, LNG-02, VEN-01, VEN-02, AUD-01, AUD-02, EVA-01
- Missing control IDs: None
- Review frequency: Quarterly
- Last review date: 2026-06-01
- Next review date: 2026-09-01
- Monitoring owner: Communications quality coordinator
- Governance flags: None

Risk note: Medium-priority public-language use when limited to approved public source text and human editorial review.

Limitations:
- Simplification can remove legally important nuance.
- Translated support text may need separate language review.

Mitigations:
- Compare simplified text with approved source before publication.
- Keep legal or rights-related wording under content-owner approval.
- Use terminology checklist for service-specific terms.

## Disclaimer

This is a deterministic public demonstration using fictional municipal examples. It is not a production system, legal assessment, compliance certification, DPIA, procurement recommendation or final AI Act classification. Internal labels such as Low, Medium, High, Critical, Approved, Approved with conditions, Restricted and Not approved are demo governance labels only.
