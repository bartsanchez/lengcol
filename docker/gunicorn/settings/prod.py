bind = "0.0.0.0:8000"

workers = 3
worker_class = "gthread"
threads = 3

accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
