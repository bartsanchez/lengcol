.PHONY: build run stop logs clean deploy tests

ENV ?= dev

build:
	docker-compose -f docker-compose.yml -f docker-compose.$(ENV).yml build

pull:
	docker-compose -f docker-compose.yml -f docker-compose.$(ENV).yml pull

run:
	docker-compose -f docker-compose.yml -f docker-compose.$(ENV).yml up -d

stop:
	docker-compose -f docker-compose.yml -f docker-compose.$(ENV).yml down

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
