.PHONY: build run start stop run logs ps clean deploy tests

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

ps:
	docker-compose -f docker-compose.yml -f docker-compose.$(ENV).yml ps

clean:
	find . -name "*.pyc" -delete

deploy:
	/bin/bash ./deployment/deploy.sh

tests:
	tox

integration_tests:
	scripts/run_integration_tests.sh
