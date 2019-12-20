from .common import wopen
from ..config import CHOICE_RES
from .file_content import git_ignore_content


def create_git_ignore(pro_name):
    print(f'Creating file: {pro_name}/.gitignore')
    with wopen(f'project/{pro_name}/.gitignore') as f:
        f.write(git_ignore_content)


def create():
    pro_name = CHOICE_RES['project_name']
    create_git_ignore(pro_name)
