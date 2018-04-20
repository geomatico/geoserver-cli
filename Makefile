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

.PHONY: doc
doc:
	@sphinx-apidoc -feo docs/source geoserver geoserver/cli
	@cd docs && make clean html

.PHONY: docker-run
docker-run:
	docker run -d -p 8080:8080 -v ${PWD}/test/geoserver_data_dir:/var/local/geoserver --name=geoserver-cli-test oscarfonts/geoserver:latest
