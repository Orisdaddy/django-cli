import os
import random
from ..config import CHOICE_RES
from .common import wopen


init_db_content = '''import pymysql

pymysql.install_as_MySQLdb()
'''

urls_content = """from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
"""

models_content = '''from django.db import models


# class User(models.Model):
#     username = models.CharField(max_length=32, unique=True)
'''


def get_random_string(length):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return ''.join(random.choice(chars) for i in range(length))


def create_application(pro_name, app_conf):
    app_name = app_conf['name']
    views = app_conf['views']
    app_path = 'project/' + pro_name + '/' + app_name

    os.makedirs(app_path)
    os.makedirs(app_path + '/migrations')
    print(f'Creating file: {app_path}/migrations/__init__.py')
    wopen(f'{app_path}/migrations/__init__.py').close()

    if views:
        os.makedirs(app_path + '/s')
    else:
        print(f'Creating file: {app_path}/views.py')
        wopen(f'{app_path}/views.py').close()

    print(f'Creating file: {app_path}/__init__.py')
    if CHOICE_RES['database'].get('engine') == 'mysql':
        with wopen(f'{app_path}/__init__.py') as f:
            f.write(init_db_content)
    else:
        wopen(f'{app_path}/__init__.py').close()
    admin_content = '''from django.contrib import admin
# from {0} import models

# admin.site.register(models.User)
'''.format(app_name)

    with wopen(f'{app_path}/admin.py') as f:
        f.write(admin_content)

    apps_content = """from django.apps import AppConfig


class App1Config(AppConfig):
    name = '{0}'
""".format(app_name)

    print(f'Creating file: {app_path}/apps.py')
    with wopen(f'{app_path}/apps.py') as f:
        f.write(apps_content)

    print(f'Creating file: {app_path}/models.py')
    with wopen(f'{app_path}/models.py') as f:
        f.write(models_content)

    print(f'Creating file: {app_path}/test.py')
    with wopen(f'{app_path}/test.py') as f:
        f.write('from django.test import TestCase')\

    return app_name


def create_project(pro_name):
    pro_path = 'project/' + pro_name + '/' + pro_name
    os.makedirs(pro_path)


def create_manage_file(pro_name):
    print('Creating file: manage.py')
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
""".format(pro_name)
    with wopen(f'project/{pro_name}/manage.py') as f:
        f.write(manage_content)
    wopen(f'project/{pro_name}/test.py').close()


def create_root_dir_file(pro_name):
    secret_key = get_random_string(50)
    pro_path = 'project/' + pro_name
    database_conf = CHOICE_RES['database']
    application_conf = CHOICE_RES['application']
    if application_conf is None:
        application = ''
    else:
        application = ''
        for app in application_conf:
            # 创建app并返回app_name
            app_name = create_application(pro_name, app)
            application += "\n\t'" + app_name + "',"
    if database_conf is None:
        database = '''{
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
'''
    else:
        engine = database_conf['engine']
        host = database_conf.get('host', '127.0.0.1')
        port = database_conf.get('port', '3306')
        db = database_conf.get('db')
        user = database_conf.get('user', 'root')
        password = database_conf.get('password', '')
        database = '''{
    'default': {
        'ENGINE': 'django.db.backends.%s',
        'NAME': '%s',
        'HOST': '%s',
        'PORT': '%s',
        'USER': '%s',
        'PASSWORD': '%s',
    }
}
''' % (engine, db, host, port, user, password)

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
""" % (secret_key, application, pro_name, pro_name, database)

    wopen(f'{pro_path}/{pro_name}/__init__.py').close()

    print(f'Creating file: {pro_name}/setting.py')
    with wopen(f'{pro_path}/{pro_name}/setting.py') as f:
        f.write(setting_content)

    print(f'Creating file: {pro_name}/urls.py')
    with wopen(f'{pro_path}/{pro_name}/urls.py') as f:
        f.write(urls_content)

    wsgi_content = """import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{0}.settings')

application = get_wsgi_application()
""".format(pro_name)
    print(f'Creating file: {pro_name}/wsgi.py')
    with wopen(f'{pro_path}/{pro_name}/wsgi.py') as f:
        f.write(wsgi_content)


def create():
    pro_name = CHOICE_RES['project_name']
    create_project(pro_name)
    create_manage_file(pro_name)
    create_root_dir_file(pro_name)

