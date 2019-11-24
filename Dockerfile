FROM debian:stable-slim

RUN apt update && \
    apt install -y python3-pip \
                   python3-psycopg2

RUN mkdir -p /opt/lengcol/
WORKDIR /opt/lengcol

COPY requirements.txt .
COPY requirements/base.txt ./requirements/
RUN pip3 install -r requirements.txt

COPY . /opt/lengcol/

WORKDIR /opt/lengcol/lengcol/

CMD ["gunicorn", "lengcol.wsgi:application", "--bind", "0.0.0.0:8000", "--access-logfile", "-"]