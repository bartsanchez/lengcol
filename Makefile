.PHONY: build run stop logs clean deploy test

ENV ?= dev

build:
	docker-compose -f docker-compose.yml -f docker-compose.$(ENV).yml build

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

test:
	pip install tox
	tox
