from .common import wopen
from ..config import CHOICE_RES

requirement = {
    'PyMySQL': False,
    'Django': True,
    'pytz': True,
    'sqlparse': True,
}


def requiretxt(pro_name):
    requirement_content = ''
    for package, vision in requirement.items():
        if isinstance(vision, bool):
            if vision is True:
                requirement_content += package + '\n'
            elif vision is False:
                pass
        else:
            requirement_content += package + '==' + vision + '\n'
    print(f'Creating file: {pro_name}/requirement.txt')
    with wopen(f'project/{pro_name}/requirement.txt') as f:
        f.write(requirement_content)


def create():
    pro_name = CHOICE_RES['project_name']
    requiretxt(pro_name)
