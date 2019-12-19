from pynput import keyboard
import os
from .config import CHOICE_RES
import subprocess


def pip_install(
        package, vision='',
        repository='-i https://pypi.tuna.tsinghua.edu.cn/simple',
        p=None
):
    if vision:
        vision = '==' + vision
    command = "pip3 install %s%s %s" % (package, vision, repository)
    if p:
        p.stdin.write(command.encode())
    else:
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    for line in iter(p.stdout.readline, b''):
        print(line.decode())
    p.stdout.close()
    p.wait()


class Choice:
    wsgi_engine_option = ['gunicorn', 'uWSGI', None]
    wsgi_mode_option = ['sync', 'gevent', 'eventlet', 'tornado', 'gaiohttp', 'gthread']

    def __print(self, desc, option, c=0):
        print(desc)
        for i, v in enumerate(option):
            if c == i:
                print('\033[1;31;40m{0}\033[0m'.format(v))
            else:
                print(v)

    def choice_wsgi_engine(self, c=0):
        self.__print(
            "选择wsgi服务器",
            self.wsgi_engine_option,
            c
        )

    def choice_wsgi_mode(self, c=0):
        self.__print(
            "选择wsgi运行模式",
            self.wsgi_mode_option,
            c
        )


choice_obj = Choice()


class CmdChoice:
    def __init__(self):
        self.choice = None
        self.choice_index = 0

    def on_press(self, key):
        x = os.system('cls')
        if key == keyboard.Key.up:
            if self.choice_index > 0:
                self.choice_index -= 1
            getattr(choice_obj, 'choice_' + self.choice)(c=self.choice_index)

        elif key == keyboard.Key.down:
            if self.choice_index < len(getattr(choice_obj, self.choice + '_option')) - 1:
                self.choice_index += 1
            getattr(choice_obj, 'choice_' + self.choice)(c=self.choice_index)

        elif key == keyboard.Key.enter:
            CHOICE_RES[self.choice] = getattr(choice_obj, self.choice + '_option')[self.choice_index]
            self.choice_index = 0
            return False

    def listen(self, choice):
        self.choice = choice
        x = os.system('cls')
        getattr(choice_obj, 'choice_' + self.choice)()
        keyboard_listener = keyboard.Listener(on_press=self.on_press)
        lst = [keyboard_listener]

        for t in lst:
            t.start()
        for t in lst:
            t.join()


cc = CmdChoice()
