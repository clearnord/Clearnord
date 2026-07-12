# Norwegian Public-Sector Language Control Report

## Executive Summary

Documents checked: 4

Total findings: 21

This report applies deterministic early-warning controls to fictional Norwegian public-sector text examples. It supports accountable human review, controlled multilingual communication and publication-readiness discussions.

## Findings by Severity

| Severity | Count |
| --- | --- |
| info | 0 |
| low | 8 |
| medium | 9 |
| high | 4 |

## Findings by Control ID

| Control ID | Count |
| --- | --- |
| HUM-01 | 1 |
| LNG-02 | 1 |
| LNG-03 | 2 |
| LNG-04 | 1 |
| LNG-05 | 1 |
| LNG-06 | 7 |
| LNG-07 | 3 |
| LNG-08 | 5 |

## Publication-Readiness Overview

| Document ID | File | Status |
| --- | --- | --- |
| clear-service-notice | 01-clear-service-notice.md | Ready for editorial review |
| nav-capitalisation | 02-nav-capitalisation.md | Ready for editorial review |
| mixed-bokmal-nynorsk | 03-mixed-bokmal-nynorsk.md | Human language review required |
| bureaucratic-internal-note | 04-bureaucratic-internal-note.md | Revision required before publication |

## Human-Review Queue

| Document ID | File | Status |
| --- | --- | --- |
| mixed-bokmal-nynorsk | 03-mixed-bokmal-nynorsk.md | Human language review required |
| bureaucratic-internal-note | 04-bureaucratic-internal-note.md | Revision required before publication |

## Frist for å sende inn dokumentasjon

- Document ID: `clear-service-notice`
- File: `01-clear-service-notice.md`
- Intended audience: Innbyggere som har fått brev om manglende dokumentasjon
- Language standard: Bokmål
- Publication channel: Kommunal serviceportal
- Citizen-facing: True
- Requires next step: True
- Content owner: Servicekontoret
- Human review required: True
- Publication-readiness status: Ready for editorial review

Clean-baseline result: no findings were produced for this document.

## Veiledning om kontakt med NAV

- Document ID: `nav-capitalisation`
- File: `02-nav-capitalisation.md`
- Intended audience: Innbyggere som trenger hjelp til å finne riktig veiledningstjeneste
- Language standard: Bokmål
- Publication channel: Kommunal serviceportal
- Citizen-facing: True
- Requires next step: True
- Content owner: Servicekontoret
- Human review required: True
- Publication-readiness status: Ready for editorial review

| Control ID | Rule title | Severity | Evidence | Line | Suggested action | Human review |
| --- | --- | --- | --- | --- | --- | --- |
| LNG-02 | Terminology and naming consistency | low | NAV / Nav | 1 | Use NAV consistently when referring to the service name. | False |

- Why LNG-02 matters: Inconsistent names can reduce trust and make service routing harder to follow.

## Utkast til informasjon om søknadsbehandling

- Document ID: `mixed-bokmal-nynorsk`
- File: `03-mixed-bokmal-nynorsk.md`
- Intended audience: Innbyggere som venter på svar om kommunal støtte
- Language standard: Bokmål
- Publication channel: Kommunal serviceportal
- Citizen-facing: True
- Requires next step: True
- Content owner: Fagavdeling for innbyggertjenester
- Human review required: True
- Publication-readiness status: Human language review required

| Control ID | Rule title | Severity | Evidence | Line | Suggested action | Human review |
| --- | --- | --- | --- | --- | --- | --- |
| LNG-03 | Written-standard consistency | medium | behandlet, dokumentene, saka, samandrag, søknaden | 3 | Route the text to human language review and choose one written-standard strategy. | True |
| LNG-03 | Written-standard consistency | medium | saka, samandrag | 3 | Align the body text with the front-matter language_standard or update the metadata after review. | True |
| LNG-06 | Clear responsibility and timing | medium | blir vurdert | 3 | Rewrite with a named actor where responsibility matters. | True |

- Why LNG-03 matters: Mixed written-standard signals can confuse readers and should be reviewed before publication.
- Why LNG-03 matters: Mixed written-standard signals can confuse readers and should be reviewed before publication.
- Why LNG-06 matters: Named responsibility and concrete timing support accountability and predictable service follow-up.

## Utkast om behandling av servicehenvendelser

- Document ID: `bureaucratic-internal-note`
- File: `04-bureaucratic-internal-note.md`
- Intended audience: Innbyggere som har sendt spørsmål til kommunen
- Language standard: Bokmål
- Publication channel: Kommunal serviceportal
- Citizen-facing: True
- Requires next step: True
- Content owner: Ikke avklart
- Human review required: False
- Publication-readiness status: Revision required before publication

| Control ID | Rule title | Severity | Evidence | Line | Suggested action | Human review |
| --- | --- | --- | --- | --- | --- | --- |
| LNG-04 | Plain-language summary | medium | No plain-language summary heading found | Not line-specific | Add a short summary that states the main message in plain language. | True |
| LNG-05 | Clear next step | medium | requires_next_step is true, but no next-step text was found | Not line-specific | Add a clear next step for the reader before publication. | True |
| LNG-08 | Bureaucratic wording early warning | low | vedrørende | 3 | Use "om" when that keeps the meaning. | False |
| LNG-08 | Bureaucratic wording early warning | low | foreligger | 7 | Use "finnes" or explain what is available. | False |
| LNG-08 | Bureaucratic wording early warning | low | iverksette | 7 | Use "starte" or "sette i gang" when suitable. | False |
| LNG-08 | Bureaucratic wording early warning | low | på nåværende tidspunkt | 7 | Use "nå" or give a concrete date. | False |
| LNG-08 | Bureaucratic wording early warning | low | i henhold til | 7 | Use "etter" or name the source requirement clearly. | False |
| LNG-06 | Clear responsibility and timing | low | senere | 7 | Replace vague timing with a concrete date, deadline or service interval. | False |
| LNG-06 | Clear responsibility and timing | low | snarest | 9 | Replace vague timing with a concrete date, deadline or service interval. | False |
| LNG-06 | Clear responsibility and timing | medium | ansvarlig enhet er ikke avklart | 9 | Name the responsible unit or role so the reader knows who is accountable. | True |
| LNG-06 | Clear responsibility and timing | medium | det vurderes | 9 | Name the responsible unit or role so the reader knows who is accountable. | True |
| LNG-06 | Clear responsibility and timing | medium | bli behandlet | 7 | Rewrite with a named actor where responsibility matters. | True |
| LNG-06 | Clear responsibility and timing | medium | det vurderes | 9 | Rewrite with a named actor where responsibility matters. | True |
| LNG-07 | Separation of internal and public content | high | INTERN MERKNAD | 5 | Remove internal workflow notes from citizen-facing text before publication. | True |
| LNG-07 | Separation of internal and public content | high | TODO | 5 | Remove internal workflow notes from citizen-facing text before publication. | True |
| LNG-07 | Separation of internal and public content | high | saksbehandler bør | 5 | Remove internal workflow notes from citizen-facing text before publication. | True |
| HUM-01 | Human review requirement | high | human_review_required: false | Not line-specific | Set human_review_required to true and route high-severity findings to an accountable reviewer. | True |

- Why LNG-04 matters: A short summary helps residents understand the main message before details.
- Why LNG-05 matters: Citizen-facing service text should explain what the reader should do next when action is expected.
- Why LNG-08 matters: Administrative expressions can make public-sector text harder to understand.
- Why LNG-08 matters: Administrative expressions can make public-sector text harder to understand.
- Why LNG-08 matters: Administrative expressions can make public-sector text harder to understand.
- Why LNG-08 matters: Administrative expressions can make public-sector text harder to understand.
- Why LNG-08 matters: Administrative expressions can make public-sector text harder to understand.
- Why LNG-06 matters: Named responsibility and concrete timing support accountability and predictable service follow-up.
- Why LNG-06 matters: Named responsibility and concrete timing support accountability and predictable service follow-up.
- Why LNG-06 matters: Named responsibility and concrete timing support accountability and predictable service follow-up.
- Why LNG-06 matters: Named responsibility and concrete timing support accountability and predictable service follow-up.
- Why LNG-06 matters: Named responsibility and concrete timing support accountability and predictable service follow-up.
- Why LNG-06 matters: Named responsibility and concrete timing support accountability and predictable service follow-up.
- Why LNG-07 matters: Internal notes in public text can expose process material and reduce public trust.
- Why LNG-07 matters: Internal notes in public text can expose process material and reduce public trust.
- Why LNG-07 matters: Internal notes in public text can expose process material and reduce public trust.
- Why HUM-01 matters: High-severity language findings should route to accountable human review before publication.

## Disclaimer

These are deterministic early-warning checks. The report does not determine
legal compliance, final linguistic correctness or whether a publication is
suitable for a specific audience.
