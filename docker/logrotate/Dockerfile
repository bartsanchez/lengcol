FROM debian:stable-slim
RUN apt update && \
    apt install -y logrotate \
                   netcat-openbsd
RUN mkdir -p /var/log/nginx/
RUN mkdir -p /var/log/gunicorn/
COPY logrotate.conf .
RUN chmod 644 logrotate.conf
