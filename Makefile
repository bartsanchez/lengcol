.PHONY: build run stop logs clean deploy test

build:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml build

run:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

stop:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml down

logs:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml logs $(ARGS)

clean:
	find . -name "*.pyc" -delete

deploy:
	/bin/bash ./deployment/deploy.sh

test:
	pip install tox
	tox
