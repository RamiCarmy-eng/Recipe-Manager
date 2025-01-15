import multiprocessing
import os

# Gunicorn configuration file

# Server socket
bind = os.getenv('GUNICORN_BIND', '0.0.0.0:8000')
backlog = 2048

# Worker processes
workers = os.getenv('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1)
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2

# Process naming
proc_name = 'recipe-manager'
pythonpath = '.'

# Logging
accesslog = 'logs/gunicorn-access.log'
errorlog = 'logs/gunicorn-error.log'
loglevel = os.getenv('GUNICORN_LOG_LEVEL', 'info')
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process management
daemon = False
pidfile = 'gunicorn.pid'
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL
keyfile = None
certfile = None

# Server mechanics
chdir = '.'
reload = os.getenv('FLASK_ENV', 'production') == 'development'
spew = False
preload_app = True
sendfile = True

# Server hooks
def on_starting(server):
    """
    Called just before the master process is initialized.
    """
    pass

def on_reload(server):
    """
    Called before code is reloaded.
    """
    pass

def when_ready(server):
    """
    Called just after the server is started.
    """
    pass

def pre_fork(server, worker):
    """
    Called just before a worker is forked.
    """
    pass

def post_fork(server, worker):
    """
    Called just after a worker has been forked.
    """
    pass

def pre_exec(server):
    """
    Called just before a new master process is forked.
    """
    pass

def pre_request(worker, req):
    """
    Called just before a request.
    """
    worker.log.debug("%s %s" % (req.method, req.path))

def post_request(worker, req, environ, resp):
    """
    Called after a request.
    """
    pass

def worker_exit(server, worker):
    """
    Called just after a worker has been exited.
    """
    pass

def worker_abort(worker):
    """
    Called when a worker received SIGABRT signal.
    """
    pass 