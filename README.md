# ClearNord

ClearNord develops practical methods, controls and demonstrations for responsible use of AI and language technology in public-sector and regulated workflows.

This repository will contain ClearNord reference frameworks, deterministic demos and documentation related to:

- AI and language governance
- controlled multilingual workflows
- human review and accountable approval
- vendor and procurement readiness
- source-grounded generative AI
- public-sector language quality
- auditability and documentation

The repository does not provide legal advice, compliance certification or production-ready public-sector software.

Website: https://clearnord.no

## Repository overview

ClearNord works at the intersection of AI, language technology,
multilingual public communication, human review and auditable workflows.

This repository contains public reference frameworks and deterministic
demos for early governance, assurance and documentation work. The intended
audience is public-sector service owners, language and communication teams,
procurement staff, data protection and security reviewers, legal-adjacent
governance teams, and technologists preparing controlled AI-supported
workflows.

The repository demonstrates practical patterns for:

- identifying AI and language-tool exposure before pilots or procurement
- documenting accountable ownership, human review and approval
- checking Norwegian public-sector language examples with deterministic rules
- structuring evidence-oriented vendor readiness questions
- refusing unsupported generated answers when approved sources are insufficient
- evaluating mock AI responses with red-team test cases

The examples use fictional data only. They do not name real municipalities,
citizens, employees, vendors or individual cases.

## What this repository does not claim

This repository does not provide legal advice, legal-compliance
determinations, certification, DPIAs, security approvals, procurement
decisions or production-ready public-sector software. The demos are not
products, and their labels are internal governance demonstration labels.

ClearNord Språkverk is a separate product under development. It is not this
repository, and this repository does not claim that Språkverk is completed or
production ready.

## Framework and language workflows

The governance framework applies to AI-assisted workflows that create,
transform, translate, summarize, classify or review language content where
quality, accountability and traceability matter. That includes AI-assisted
translation, document work, source-grounded drafting, simplification and
multilingual public communication.

The common thread is controlled use: approved source material where relevant,
clear human responsibility, documented review, careful treatment of language
quality, and audit evidence that can be reviewed later.

## Repository map

- Framework: [Public-sector AI and language governance](frameworks/public-sector-ai-language-governance.md)
- AI and language exposure register: [demo README](demos/ai-language-exposure-register/README.md)
- Norwegian language controls: [demo README](demos/norwegian-language-controls/README.md)
- Vendor readiness scorecard: [demo README](demos/vendor-readiness-scorecard/README.md)
- Grounded answer transparency: [demo README](demos/grounded-answer-transparency/README.md)
- Red-team evaluation kit: [demo README](demos/red-team-evaluation-kit/README.md)

## Run the complete suite

Use Python 3.11 or newer.

```bash
python -m pip install -r requirements.txt
make generate
make test
python run_all.py
git diff --exit-code
```

`make generate` regenerates all committed Markdown reports, including
`SUITE_REPORT.md`. `make test` runs all demo tests. `make verify` combines
generation, tests and a committed-report diff check.

The suite is deterministic. It uses fixed run identifiers and does not call
external APIs.
