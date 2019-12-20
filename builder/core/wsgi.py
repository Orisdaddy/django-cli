from .common import wopen
from ..config import CHOICE_RES


def create_gunicorn_config(pro_name, worker_class):
    content = '''import multiprocessing

bind = '0.0.0.0:8080'
timeout = 30
worker_class = '{0}'
workers = multiprocessing.cpu_count()*2 + 1
threads = 2
'''.format(worker_class)
    print(f'Creating file: {pro_name}/gunicorn.py')
    with wopen(f'project/{pro_name}/gunicorn.py') as f:
        f.write(content)


def create_uwsgi_config(pro_name, worker_class):
    content = '''[uwsgi]

http=0.0.0.0:8000
master = true
harakiri = 30
processes = 9
'''
    print(f'Creating file: {pro_name}/uWSGI.ini')
    with wopen(f'project/{pro_name}/uWSGI.ini') as f:
        f.write(content)


def create():
    pro_name = CHOICE_RES['project_name']
    wsgi_engine = CHOICE_RES['wsgi_engine']
    wsgi_mode = CHOICE_RES['wsgi_mode']
    if wsgi_engine == 'gunicorn':
        create_gunicorn_config(pro_name, wsgi_mode)
    elif wsgi_engine == 'uWSGI':
        create_uwsgi_config(pro_name, wsgi_mode)
