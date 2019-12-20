"""
python-vision: 3.x

启动:
python cli.py
"""
import subprocess
from builder.config import CHOICE_RES, Config
from builder import script
from builder.core import require, project, wsgi, git, venv


def start():
    # 安装键位控制包
    script.pip_install('pynput', output=False)
    listen = script.cc.listen
    # 项目名称
    project_name = CHOICE_RES['project_name']
    while not project_name:
        project_name = input("项目名称:")
    CHOICE_RES['project_name'] = project_name
    # 选择导入构建配置文件
    conf = None
    while conf is None:
        conf = input("是否读取配置文件构建项目(y/N):")
        if conf.upper() == 'Y':
            CHOICE_RES['django_vision'] = Config['django_vision']
            CHOICE_RES['wsgi_engine'] = Config['wsgi']['engine']
            CHOICE_RES['wsgi_mode'] = Config['wsgi']['mode']
            CHOICE_RES['application'] = Config['application']
            CHOICE_RES['database'] = Config['database']
            CHOICE_RES['docker'] = Config['docker']
            require.requirement['Django'] = Config['django_vision']
            if Config['wsgi']['engine']:
                require.requirement[Config['wsgi']['engine']] = True
            if Config['database'].get('engine') == 'mysql':
                require.requirement['PyMySQL'] = True

        else:
            # 选择django版本
            django_vision = CHOICE_RES['django_vision']
            while not django_vision:
                django_vision = input("选择要构建的django版本 (1.1.11):")
            CHOICE_RES['django_vision'] = django_vision
            require.requirement['Django'] = django_vision

            # 选择wsgi服务器
            listen('wsgi_engine')
            wsgi_engine = CHOICE_RES['wsgi_engine']
            if wsgi_engine is not None:
                require.requirement[wsgi_engine] = True
                listen('wsgi_mode')
    # 开始创建项目
    project.create()
    require.create()
    wsgi.create()
    git.create()

    # 构建虚拟环境内容
    dev = 'z'
    while dev.upper() != 'Y' and dev.upper() != 'N' and dev:
        dev = input("是否在本地构建开发环境(Y/n):")
        if dev.upper() == 'Y' or not dev:
            dev_name = input(f"虚拟环境的名称(venv):")
            if not dev_name:
                dev_name = 'venv'
            venv.create_env(dev_name)


def run():
    start()


if __name__ == '__main__':
    run()
