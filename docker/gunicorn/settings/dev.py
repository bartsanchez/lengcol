bind = "0.0.0.0:8000"

worker_class = "gevent"
workers = 3

accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
