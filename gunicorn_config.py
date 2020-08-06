import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
bind = 'unix:dyspochat_webservice.sock'
umask = 0o777
reload = True

accesslog = "access.log"
errorlog = "error.log"