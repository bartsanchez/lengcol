FROM python:3.8-slim

RUN apt update && apt install -y python3-psycopg2

RUN mkdir -p /var/log/gunicorn/
RUN touch /var/log/gunicorn/access.log
RUN touch /var/log/gunicorn/error.log
RUN chmod 640 /var/log/gunicorn/access.log
RUN chmod 640 /var/log/gunicorn/error.log

RUN mkdir -p /opt/lengcol/
WORKDIR /opt/lengcol

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /opt/lengcol/

WORKDIR /opt/lengcol/lengcol/

CMD ["gunicorn", "lengcol.wsgi:application", "--bind", "0.0.0.0:8000", "--access-logfile", "-"]
