def create_git_ignore(pro_name):
    content = '''__pycache__/
*.py[cod]
*$py.class

*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
'''
