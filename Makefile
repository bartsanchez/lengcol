build:
	docker-compose build

run:
	docker-compose up -d

stop:
	docker-compose down

clean:
	find . -name "*.pyc" -delete

test:
	pip install tox
	tox
