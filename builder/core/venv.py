from ..script import pip_install
from ..config import CHOICE_RES
import subprocess


def create_env(venv_name):
    pro_name = CHOICE_RES['project_name']
    pip_install('virtualenv')
    p = subprocess.Popen(f"cd project/ & virtualenv {venv_name}", shell=True)
    p.wait()

    # 下载python package
    p = subprocess.Popen(
        rf"cd project/{venv_name}/Scripts & activate & cd ../../{pro_name} & pip3 install -r requirement.txt -i https://pypi.tuna.tsinghua.edu.cn/simple",
        shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE
    )
    for line in iter(p.stdout.readline, b''):
        print(line.decode())
    p.stdout.close()
    p.wait()
