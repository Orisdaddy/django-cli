import os
import random
from ..config import CHOICE_RES
from .common import wopen
from .file_content import *


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
        os.makedirs(app_path + '/views')
    else:
        print(f'Creating file: {app_path}/views.py')
        wopen(f'{app_path}/views.py').close()

    print(f'Creating file: {app_path}/__init__.py')
    if CHOICE_RES['database'].get('engine') == 'mysql':
        with wopen(f'{app_path}/__init__.py') as f:
            f.write(init_db_content)
    else:
        wopen(f'{app_path}/__init__.py').close()

    with wopen(f'{app_path}/admin.py') as f:
        f.write(admin_content.format(app_name))

    print(f'Creating file: {app_path}/apps.py')
    with wopen(f'{app_path}/apps.py') as f:
        f.write(apps_content.format(app_name))

    print(f'Creating file: {app_path}/models.py')
    with wopen(f'{app_path}/models.py') as f:
        f.write(models_content)

    print(f'Creating file: {app_path}/test.py')
    with wopen(f'{app_path}/test.py') as f:
        f.write('from django.test import TestCase')
    django_vision = CHOICE_RES['django_vision']
    if django_vision.startswith('1'):
        urls_content = '''from django.conf.urls import url

urlpatterns = [

]
'''
    else:
        urls_content = '''from django.urls import path, include

urlpatterns = [

]
'''
    print(f'Creating file: {app_path}/urls.py')
    with wopen(f'{app_path}/urls.py') as f:
        f.write(urls_content)

    return app_name


def create_project(pro_name):
    pro_path = 'project/' + pro_name + '/' + pro_name
    templates_path = 'project/' + pro_name + '/templates'
    os.makedirs(pro_path)
    os.makedirs(templates_path)


def create_manage_file(pro_name):
    print('Creating file: manage.py')
    with wopen(f'project/{pro_name}/manage.py') as f:
        f.write(manage_content.format(pro_name))
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
            application += "\r\n\t'" + app_name + "',"
    if not database_conf:
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
    wopen(f'{pro_path}/{pro_name}/__init__.py').close()
    print(f'Creating file: {pro_name}/setting.py')
    with wopen(f'{pro_path}/{pro_name}/setting.py') as f:
        f.write(setting_content % (secret_key, application, pro_name, pro_name, database))
    django_vision = CHOICE_RES['django_vision']
    if django_vision.startswith('1'):
        from_url = 'from django.conf.urls import url, include'
    else:
        from_url = 'from django.urls import path, include'
    url_app = ''
    if application_conf:
        for i, app in enumerate(application_conf):
            app_name = app['name']

            if django_vision.startswith('1'):
                if i == 0:
                    url_app += f"\turl(r'^admin/', admin.site.urls),\r\n"
                url_app += f"\turl('', include('{app_name}.urls')),\r\n"
            else:
                if i == 0:
                    url_app += f"\tpath('admin/', admin.site.urls),\r\n"
                url_app += f"\tpath('', include('{app_name}.urls')),\r\n"
    else:
        if django_vision.startswith('1'):
            url_app = f"\turl(r'^admin/', admin.site.urls),\r\n"
        else:
            url_app = f"\tpath('admin/', admin.site.urls),\r\n"

    urls_content = """from django.contrib import admin
{0}

urlpatterns = [
{1}
]
""".format(from_url, url_app)

    print(f'Creating file: {pro_name}/urls.py')
    with wopen(f'{pro_path}/{pro_name}/urls.py') as f:
        f.write(urls_content)

    print(f'Creating file: {pro_name}/wsgi.py')
    with wopen(f'{pro_path}/{pro_name}/wsgi.py') as f:
        f.write(wsgi_content.format(pro_name))

    if django_vision.startswith('3'):
        print(f'Creating file: {pro_name}/asgi.py')
        with wopen(f'{pro_path}/{pro_name}/asgi.py') as f:
            f.write(asgi_content.format(pro_name))


def create():
    pro_name = CHOICE_RES['project_name']
    create_project(pro_name)
    create_manage_file(pro_name)
    create_root_dir_file(pro_name)

