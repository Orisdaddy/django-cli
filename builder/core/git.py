from .common import wopen
from ..config import CHOICE_RES


def create_git_ignore(pro_name):
    content = '''__pycache__/
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

    print(f'Creating file: {pro_name}/.gitignore')
    with wopen(f'project/{pro_name}/.gitignore') as f:
        f.write(content)


def create():
    pro_name = CHOICE_RES['project_name']
    create_git_ignore(pro_name)
