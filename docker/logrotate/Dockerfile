FROM debian:buster-slim@sha256:06a7bee0f90b6087f2b239125ef3c75d474e48cc69643d496d0c6e545fd91023
RUN apt-get update \
 && apt-get install --no-install-recommends -y \
    logrotate \
    netcat-openbsd \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /var/log/nginx/
RUN mkdir -p /var/log/gunicorn/
COPY logrotate.conf .
RUN chmod 644 logrotate.conf
