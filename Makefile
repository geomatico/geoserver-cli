.PHONY: test
test:
	@echo =============================== TEST ================================
	@coverage run -m unittest discover -v

.PHONY: coverage
coverage: test
	@echo ============================= COVERAGE ==============================
	@coverage report --omit="*__init__.py","test/*"

.PHONY: coverage-html
coverage-html: test
	@echo ============================= COVERAGE ==============================
	@echo -n Creating coverage report...
	@coverage html --omit="*__init__.py","test/*"
	@echo Done!	

doc:
	@cd docs && make html
