from .common import wopen
from ..config import CHOICE_RES
from .file_content import gunicorn_content, uwsgi_content


def create_gunicorn_config(pro_name, worker_class):
    print(f'Creating file: {pro_name}/gunicorn.py')
    with wopen(f'project/{pro_name}/gunicorn.py') as f:
        f.write(gunicorn_content.format(worker_class))


def create_uwsgi_config(pro_name, worker_class):
    print(f'Creating file: {pro_name}/uWSGI.ini')
    with wopen(f'project/{pro_name}/uWSGI.ini') as f:
        f.write(uwsgi_content)


def create():
    pro_name = CHOICE_RES['project_name']
    wsgi_engine = CHOICE_RES['wsgi_engine']
    wsgi_mode = CHOICE_RES['wsgi_mode']
    if wsgi_engine == 'gunicorn':
        create_gunicorn_config(pro_name, wsgi_mode)
    elif wsgi_engine == 'uWSGI':
        create_uwsgi_config(pro_name, wsgi_mode)
