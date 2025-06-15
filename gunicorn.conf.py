import multiprocessing
import os

bind = os.getenv("GUNICORN_BIND", "0.0.0.0:8000")
workers = int(os.getenv("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1))
threads = int(os.getenv("GUNICORN_THREADS", 1))
timeout = int(os.getenv("GUNICORN_TIMEOUT", 120))
reload = os.getenv("GUNICORN_RELOAD", "False").lower() in ["true", "1", "yes"]

worker_class = os.getenv("GUNICORN_WORKER_CLASS", "gthread")

accesslog = os.getenv("GUNICORN_ACCESS_LOGFILE", "-")
errorlog = os.getenv("GUNICORN_ERROR_LOGFILE", "-")
loglevel = os.getenv("GUNICORN_LOGLEVEL", "info")
