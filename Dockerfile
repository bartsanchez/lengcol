FROM python:3.9-slim

LABEL maintainer="Bartolome Sanchez Salado"

ENV ENVIRONMENT dev

RUN apt-get update \
 && apt-get install --no-install-recommends -y \
    python3-psycopg2 \
    git \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/log/gunicorn/
RUN touch /var/log/gunicorn/access.log
RUN touch /var/log/gunicorn/error.log
RUN chmod 640 /var/log/gunicorn/access.log
RUN chmod 640 /var/log/gunicorn/error.log

RUN mkdir -p /var/log/celery/
RUN touch /var/log/celery/worker.log
RUN chmod 640 /var/log/celery/worker.log

RUN mkdir -p /opt/lengcol/
WORKDIR /opt/lengcol

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY . /opt/lengcol/

WORKDIR /opt/lengcol/lengcol/

EXPOSE 8000

CMD ["sh", "-c", "gunicorn lengcol.wsgi:application -c ../docker/gunicorn/settings/${ENVIRONMENT}.py"]
