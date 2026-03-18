import os
from datetime import datetime
from .json_config import Config


def datecommit() -> int:
    now = datetime.now()
    code = 0
    for command in ('git add .', f'git commit -m \"{now.strftime("%Y-%m-%d %H:%M:%S")}\"'):
        if code != 0: break
        code = os.system(command)
    return code


def commit(hrenpack_only: bool):
    directory = Config()['directory']
    code = 0
    if not hrenpack_only:
        code = datecommit()
    if code == 0:
        os.chdir(directory)
        code = datecommit()
        os.chdir('..')
    return code


def push(hrenpack_only: bool):
    directory = Config()['directory']
    code = 0
    if not hrenpack_only:
        code = os.system(f'git push origin')
    if code == 0:
        os.chdir(directory)
        code = os.system(f'git push origin')
        os.chdir('..')
    return code
