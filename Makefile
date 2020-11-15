.PHONY: build run start stop run logs clean deploy tests

ENV ?= dev
START_SERVICES ?=
RUN_SERVICE ?=

build:
	docker-compose -f docker-compose.yml -f docker-compose.$(ENV).yml build

pull:
	docker-compose -f docker-compose.yml -f docker-compose.$(ENV).yml pull

start:
	docker-compose -f docker-compose.yml -f docker-compose.$(ENV).yml up -d $(START_SERVICES)

stop:
	docker-compose -f docker-compose.yml -f docker-compose.$(ENV).yml down

run:
	docker-compose -f docker-compose.yml -f docker-compose.$(ENV).yml run $(RUN_SERVICE)

logs:
	docker-compose -f docker-compose.yml -f docker-compose.$(ENV).yml logs $(ARGS)

clean:
	find . -name "*.pyc" -delete

deploy:
	/bin/bash ./deployment/deploy.sh

tests:
	pip install tox
	tox

integration_tests:
	scripts/run_integration_tests.sh
