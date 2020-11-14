FROM python:3.9-slim

LABEL maintainer="Bartolome Sanchez Salado"

RUN mkdir -p /opt/lengcol_tests/
WORKDIR /opt/lengcol_tests

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY integration .

CMD ["pytest"]
