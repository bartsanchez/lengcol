[![Unit tests status](https://github.com/bartsanchez/lengcol/workflows/UnitTests/badge.svg?branch=master)](https://github.com/bartsanchez/lengcol/actions?query=branch%3Amaster+workflow%3AUnitTests)
[![Integration tests status](https://github.com/bartsanchez/lengcol/workflows/IntegrationTests/badge.svg?branch=master)](https://github.com/bartsanchez/lengcol/actions?query=branch%3Amaster+workflow%3AIntegrationTests)
[![codecov](https://codecov.io/gh/bartsanchez/lengcol/branch/master/graph/badge.svg)](https://codecov.io/gh/bartsanchez/lengcol)

# Lenguaje coloquial project

## Requirements

[docker](https://www.docker.com/)

[docker-compose](https://docs.docker.com/compose/)

## Run locally

```sh
$ cp example_env .env

$ make start

$ make stop
```

## Testing

### Requirements

[pip](https://pypi.org/project/pip/)

### Run tests

Simply, run:

```sh
$ make tests
$ make integration_tests
```
