build:
	docker-compose build

test:
	pip install tox
	tox
