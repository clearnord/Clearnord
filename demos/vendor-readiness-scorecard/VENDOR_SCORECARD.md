# Vendor Readiness Scorecard

## Executive Summary

Vendor name: Nordic Public AI Demo Platform

Fictional assessment ID: CN-VENDOR-DEMO-2026-07-01

Traffic-light result: Yellow: clarification or compensating controls required before pilot

Weighted score: 71.1

Hard-stop summary: No hard stops triggered.

## Score By Control Domain

| Domain | Score |
| --- | ---: |
| Auditability | 65.4 |
| Data lifecycle | 76.5 |
| Data processing | 100.0 |
| Exit and portability | 70.8 |
| Governance support | 50.0 |
| Human oversight | 100.0 |
| Incident readiness | 50.0 |
| Language and accessibility | 60.7 |
| Model transparency | 50.0 |
| Security | 80.8 |
| Vendor transparency | 50.0 |

## Detailed Question Results

| Question ID | Control ID | Domain | Answer | Weight |
| --- | --- | --- | --- | ---: |
| processing_location | VEN-02 | Data processing | eea_documented | 7 |
| customer_data_training | VEN-03 | Data processing | restricted | 8 |
| retention | VEN-04 | Data lifecycle | documented_configurable | 5 |
| deletion_verification | VEN-04 | Data lifecycle | deletion_only | 8 |
| admin_logging | AUD-01 | Auditability | yes | 4 |
| user_activity_logging | AUD-01 | Auditability | partial | 4 |
| audit_export | AUD-02 | Auditability | partial | 5 |
| human_oversight | HUM-01 | Human oversight | yes | 8 |
| explainability | VEN-01 | Model transparency | partial | 4 |
| dpia_support | VEN-01 | Governance support | partial | 4 |
| security_documentation | SEC-01 | Security | current | 8 |
| access_control | SEC-02 | Security | partial | 5 |
| subprocessors | VEN-05 | Vendor transparency | partial | 5 |
| incident_notification | VEN-06 | Incident readiness | needs_clarification | 8 |
| accessibility | LNG-01 | Language and accessibility | incomplete | 4 |
| bokmal_support | LNG-01 | Language and accessibility | tested | 3 |
| nynorsk_support | LNG-01 | Language and accessibility | partial | 3 |
| terminology_testing | LNG-01 | Language and accessibility | partial | 4 |
| data_exportability | VEN-07 | Exit and portability | yes | 5 |
| exit_transition | VEN-07 | Exit and portability | partial | 4 |
| vendor_lock_in | VEN-07 | Exit and portability | partial | 3 |
| retention_configuration | VEN-04 | Data lifecycle | yes | 4 |
| model_change_notice | VEN-01 | Model transparency | limited_notice | 5 |
| evidence_quality | VEN-01 | Governance support | mixed | 5 |

## Evidence Supplied

- access_control: Role model described, but delegation rules need clarification.
- accessibility: Accessibility test is planned but not complete.
- admin_logging: Administrative logging guide.
- audit_export: Export available on request, no self-service sample supplied.
- bokmal_support: Bokmal language quality sample provided.
- customer_data_training: Vendor states customer data is excluded from shared-model training.
- data_exportability: Export guide covers documents and logs.
- deletion_verification: Deletion workflow described, but verification report is not yet available.
- dpia_support: Data protection questionnaire available.
- evidence_quality: Several answers are supported only by vendor statements.
- exit_transition: Exit responsibilities are described but not in contract wording.
- explainability: Model limitations are documented at product level.
- human_oversight: Workflow supports human review queues and stop status.
- incident_notification: Incident process described, contractual responsibilities need clarification.
- model_change_notice: Material model updates may occur without sufficient advance notice.
- nynorsk_support: Nynorsk quality not fully tested.
- processing_location: EEA hosting statement and regional architecture note.
- retention: Retention policy and tenant settings guide.
- retention_configuration: Tenant retention settings documented.
- security_documentation: Current security whitepaper and access overview.
- subprocessors: Subprocessor list exists, change notice timing needs review.
- terminology_testing: General terminology examples supplied, no municipal test set.
- user_activity_logging: User activity logging described for core actions only.
- vendor_lock_in: Lock-in risk described; migration tooling not demonstrated.

## Missing Or Weak Evidence

- access_control
- accessibility
- audit_export
- customer_data_training
- deletion_verification
- dpia_support
- evidence_quality
- exit_transition
- explainability
- incident_notification
- model_change_notice
- nynorsk_support
- subprocessors
- terminology_testing
- user_activity_logging
- vendor_lock_in

## Unanswered Questions

- None

## Required Clarification Before Pilot

- access_control: Clarify administrator and reviewer roles.
- accessibility: Provide accessibility test summary.
- admin_logging: Confirm export format.
- audit_export: Provide sample audit export.
- bokmal_support: Confirm public-sector terminology coverage.
- customer_data_training: Convert statement into contractual restriction.
- data_exportability: Confirm export during contract exit.
- deletion_verification: Provide deletion verification evidence before pilot.
- dpia_support: Add municipal workflow assumptions.
- evidence_quality: Replace vendor statements with documentary evidence.
- exit_transition: Add transition support clause.
- explainability: Provide workflow-specific limitations.
- human_oversight: Confirm role configuration.
- incident_notification: Define notification times, roles and affected-data information.
- model_change_notice: Define advance notice for material model changes.
- nynorsk_support: Provide Nynorsk test evidence before citizen-facing pilot.
- processing_location: Confirm whether all support access also remains in the EEA.
- retention: Confirm default retention for audit logs.
- retention_configuration: Confirm who may change settings.
- security_documentation: Provide latest independent test summary under NDA.
- subprocessors: Confirm notice period for material changes.
- terminology_testing: Test public-sector terminology before pilot.
- user_activity_logging: Confirm prompt, file and output logging boundaries.
- vendor_lock_in: Demonstrate export and transition process.

## Suggested Contractual Safeguards

- access_control: Use least-privilege pilot role set.
- accessibility: Limit citizen-facing use until accessibility review is complete.
- admin_logging: Require admin log retention during pilot.
- audit_export: Include audit export service level.
- bokmal_support: Add municipal terminology checklist.
- customer_data_training: Add no-training clause for prompts, files, outputs and logs.
- data_exportability: Run export rehearsal during pilot.
- deletion_verification: Require deletion confirmation and audit trail.
- dpia_support: Require DPIA support workshop if personal data is tested.
- evidence_quality: Maintain evidence index for pilot approval.
- exit_transition: Include exit assistance and deletion verification.
- explainability: Include limitation notice in pilot records.
- human_oversight: Require named municipal approver before external use.
- incident_notification: Add incident notification clause before pilot.
- model_change_notice: Require notification and regression review for material model changes.
- nynorsk_support: Require human language review for Nynorsk outputs.
- processing_location: Include processing-location warranty in pilot terms.
- retention: Attach retention schedule to pilot approval.
- retention_configuration: Restrict retention changes to named administrators.
- security_documentation: Security owner must review before pilot.
- subprocessors: Require subprocessor change notification.
- terminology_testing: Use approved terminology list.
- user_activity_logging: Define minimum activity events for pilot.
- vendor_lock_in: Avoid proprietary-only knowledge base formats.

## Recommended Next Step

Resolve evidence gaps and contractual clarifications before any controlled pilot.

## Disclaimer

This deterministic demonstration supports early governance and assurance
work. It does not provide legal advice, compliance certification, a final
procurement decision, a DPIA, a security approval or a production-readiness
determination.
