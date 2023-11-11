.PHONY: build run start stop run logs ps clean deploy tests

ENV ?= dev
START_SERVICES ?=
RUN_SERVICE ?=

COMPOSE_EXEC ?= docker compose

build:
	${COMPOSE_EXEC} -f docker-compose.yml -f docker-compose.$(ENV).yml build

pull:
	${COMPOSE_EXEC} -f docker-compose.yml -f docker-compose.$(ENV).yml pull

start:
	${COMPOSE_EXEC} -f docker-compose.yml -f docker-compose.$(ENV).yml up -d $(START_SERVICES)

stop:
	${COMPOSE_EXEC} -f docker-compose.yml -f docker-compose.$(ENV).yml down

run:
	${COMPOSE_EXEC} -f docker-compose.yml -f docker-compose.$(ENV).yml run $(RUN_SERVICE)

logs:
	${COMPOSE_EXEC} -f docker-compose.yml -f docker-compose.$(ENV).yml logs $(ARGS)

ps:
	${COMPOSE_EXEC} -f docker-compose.yml -f docker-compose.$(ENV).yml ps

clean:
	find . -name "*.pyc" -delete

deploy:
	/bin/bash ./deployment/deploy.sh

tests:
	tox

integration_tests:
	scripts/run_integration_tests.sh
