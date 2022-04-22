FROM python:3.9-slim@sha256:ba3b77ddbc953cdb8d998b2052088d4af4b8805805e5b01975a05af4e19855ea

LABEL maintainer="Bartolome Sanchez Salado"

RUN mkdir -p /opt/lengcol_tests/
WORKDIR /opt/lengcol_tests

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY integration .

CMD ["pytest"]
