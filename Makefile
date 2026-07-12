PYTHON ?= python

GENERATED_REPORTS = \
	demos/ai-language-exposure-register/EXPOSURE_REGISTER.md \
	demos/norwegian-language-controls/LANGUAGE_CONTROL_REPORT.md \
	demos/vendor-readiness-scorecard/VENDOR_SCORECARD.md \
	demos/grounded-answer-transparency/ANSWER_LOG.md \
	demos/red-team-evaluation-kit/EVALUATION_REPORT.md \
	SUITE_REPORT.md

.PHONY: install generate test verify clean

install:
	$(PYTHON) -m pip install -r requirements.txt

generate:
	$(PYTHON) run_all.py

test:
	$(PYTHON) -m pytest \
		demos/ai-language-exposure-register/tests \
		demos/norwegian-language-controls/tests \
		demos/vendor-readiness-scorecard/tests \
		demos/grounded-answer-transparency/tests \
		demos/red-team-evaluation-kit/tests \
		--basetemp=.pytest-basetemp \
		-q

verify: generate test
	git diff --exit-code -- $(GENERATED_REPORTS)

clean:
	$(PYTHON) -c "from pathlib import Path; import shutil; [shutil.rmtree(p, ignore_errors=True) for p in Path('.').rglob('__pycache__')]; shutil.rmtree('.pytest_cache', ignore_errors=True); shutil.rmtree('.pytest-basetemp', ignore_errors=True)"
