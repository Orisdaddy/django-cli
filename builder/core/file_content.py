git_ignore_content = '''__pycache__/
*.py[cod]
*$py.class

.idea/
.vscode/

*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

env/
venv/
'''

init_db_content = '''import pymysql

pymysql.install_as_MySQLdb()
'''

models_content = '''from django.db import models


# class User(models.Model):
#     username = models.CharField(max_length=32, unique=True)
'''

admin_content = '''from django.contrib import admin
# from {0} import models

# admin.site.register(models.User)
'''

apps_content = """from django.apps import AppConfig


class App1Config(AppConfig):
    name = '{0}'
"""


manage_content = """import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{0}.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
"""

setting_content = """import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '%s'


DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',%s
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '%s.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = '%s.wsgi.application'

DATABASES = %s

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
"""


wsgi_content = """import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{0}.settings')

application = get_wsgi_application()
"""

asgi_content = """import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{0}.settings')

application = get_asgi_application()
"""

gunicorn_content = '''import multiprocessing

bind = '0.0.0.0:8080'
timeout = 30
worker_class = '{0}'
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
'''

uwsgi_content = '''[uwsgi]

http=0.0.0.0:8000
master = true
harakiri = 30
processes = 9
'''