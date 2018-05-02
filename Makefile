.PHONY: test
test:
	@echo =============================== TEST ================================
	@coverage run -m unittest discover -v

.PHONY: coverage
coverage: test
	@echo ============================= COVERAGE ==============================
	@coverage report --omit="*__init__.py","test/*","env/*"

.PHONY: coverage-html
coverage-html: test
	@echo ============================= COVERAGE ==============================
	@echo -n Creating coverage report...
	@rm -rf htmlcov
	@coverage html --omit="*__init__.py","test/*","env/*"
	@echo Done!

.PHONY: doc
doc:
	@sphinx-apidoc -feo docs/source geoserver geoserver/cli
	@cd docs && make clean html

.PHONY: docker-run-latest
docker-run-latest:
	@rm -rf test/data
	@cp -r test/geoserver_data_dir test/data
	docker run -d -p 8080:8080 -v ${PWD}/test/data:/var/local/geoserver --name=geoserver-cli-test oscarfonts/geoserver:latest

.PHONY: docker-run-maintenance
docker-run-maintenance:
	@rm -rf test/data
	@cp -r test/geoserver_data_dir test/data
	docker run -d -p 8080:8080 -v ${PWD}/test/data:/var/local/geoserver --name=geoserver-cli-test-maintenance oscarfonts/geoserver:2.12.2
