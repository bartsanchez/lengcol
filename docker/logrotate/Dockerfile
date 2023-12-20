FROM debian:bookworm-20231218
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
