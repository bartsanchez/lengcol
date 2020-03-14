FROM debian:stable-slim
RUN apt update && \
    apt install -y logrotate
COPY logrotate.conf .
RUN chmod 644 logrotate.conf
