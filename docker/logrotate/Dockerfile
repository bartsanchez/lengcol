FROM debian:stable-slim
RUN apt update && \
    apt install -y logrotate \
                   netcat-openbsd
COPY logrotate.conf .
RUN chmod 644 logrotate.conf
