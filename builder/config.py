Config = {
    'django_vision': '2.2.6',
    'wsgi': {
        # 'engine': 'gunicorn',  # gunicorn/uWSGI/None
        'engine': None,  # gunicorn/uWSGI/None
        'mode': 'gevent'
    },

    'application': [
        {
            'name': 'app1',
            'views': False,
        }
    ],
    'database': {},
    # 'database': {
    #     'engine': 'mysql',
    #     'host': '127.0.0.1',
    #     'port': '3306',
    #     'db': 'db123',
    #     'user': 'root',
    #     'password': '123456',
    # },

    'docker': {}
}


# 不要修改CHOICE_RES
CHOICE_RES = {
    'project_name': None,
    'wsgi_engine': None,
    'wsgi_mode': None,
    'django_vision': '1.11.11',
    'dev_env': False,
    'env_name': '',
    'application': None,
    'database': None,
    'docker': None,
}
