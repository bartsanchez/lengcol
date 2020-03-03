build:
	docker-compose build

run:
	docker-compose up -d

test:
	pip install tox
	tox
