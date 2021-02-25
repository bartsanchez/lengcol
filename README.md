[![Unit tests status](https://github.com/bartsanchez/lengcol/workflows/UnitTests/badge.svg?branch=master)](https://github.com/bartsanchez/lengcol/actions?query=branch%3Amaster+workflow%3AUnitTests)
[![Integration tests status](https://github.com/bartsanchez/lengcol/workflows/IntegrationTests/badge.svg?branch=master)](https://github.com/bartsanchez/lengcol/actions?query=branch%3Amaster+workflow%3AIntegrationTests)
[![codecov](https://codecov.io/gh/bartsanchez/lengcol/branch/master/graph/badge.svg)](https://codecov.io/gh/bartsanchez/lengcol)

# Lenguaje coloquial project

## Features

- Continuous Integration Development using [Github actions](https://github.com/bartsanchez/lengcol/actions)
- [TLS 1.3 A+](https://www.ssllabs.com/ssltest/analyze.html?d=lenguajecoloquial.com)
- Domain included in HTTP Strict Transport Security (HSTS) [preload list](https://hstspreload.org/?domain=lenguajecoloquial.com)
- [Google Recaptcha V3](https://developers.google.com/recaptcha)
- Metrics collection with [Prometheus](https://prometheus.io/)

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

[tox](https://tox.readthedocs.io/)

### Run tests

Simply, run:

```sh
$ make tests
$ make integration_tests
```
