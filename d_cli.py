"""
python-vision: 3.x
"""
import subprocess
from builder.config import CHOICE_RES, Config
from builder import script
from builder.core import require, project, wsgi, git


def start():
    # 安装键位控制包
    script.pip_install('pynput')
    listen = script.cc.listen
    # 项目名称
    project_name = CHOICE_RES['project_name']
    while not project_name:
        project_name = input("项目名称:")
        print('\033[1;35;0m字体变色，但无背景色 \033[0m')
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
            require.requirement[Config['wsgi']['engine']] = True
            require.requirement['PyMySQL'] = True

        else:
            # 选择django版本
            django_vision = CHOICE_RES['django_vision']
            while not django_vision:
                django_vision = input("选择django版本:")
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

    # 构建虚拟环境内容
    # dev = 'z'
    # while dev.upper() == 'Y' or dev.upper() == 'N':
    #     dev = input("是否在本地构建开发环境(y/n):")
    #     if dev.upper() == 'Y':
    #         CHOICE_RES['dev_env'] = True
    #         dev_name = input(f"虚拟环境的名称({project_name}_venv):")
    #     elif dev.upper() == 'N':
    #         CHOICE_RES['dev_env'] = False


def create_env(venv_name):
    script.pip_install('virtualenv')
    p = subprocess.Popen(f"virtualenv {venv_name}", shell=True)
    p.wait()
    django_vision = input("选择要构建的django版本 (1.1.11):")

    if django_vision == '':
        django_vision = '1.11.11'
    # 下载django
    CHOICE_RES['django_vision'] = django_vision
    django_vision = '==' + django_vision
    p = subprocess.Popen(
        rf"cd {venv_name}\Scripts & activate & pip3 install django{django_vision} -i https://pypi.tuna.tsinghua.edu.cn/simple",
        shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE
    )
    for line in iter(p.stdout.readline, b''):
        print(line.decode())
    p.stdout.close()
    p.wait()


def run():
    start()


if __name__ == '__main__':
    run()
