.PHONY: build run stop clean deploy test

build:
	docker-compose build

run:
	docker-compose up -d

stop:
	docker-compose down

clean:
	find . -name "*.pyc" -delete

deploy:
	/bin/bash ./deployment/deploy.sh

test:
	pip install tox
	tox
