import os, sys
from typing import Literal, List, Optional
from typer import Typer, Argument, Option
from . import commands
from .json_config import Config

app = Typer(no_args_is_help=True)


@app.command
def clone(directory: str = Argument('hrenpack_source', help="Directory to clone")):
    config = Config()
    config['directory'] = directory
    sys.exit(os.system(f'git clone https://github.com/MagIlyasDOMA/hrenpack.git {directory}'))


@app.command
def managers(action: Optional[Literal['add', 'remove', 'set']] = Argument(None, help="Action to perform"),
             args: Optional[List[Literal['uv', 'pipenv', 'npm', 'yarn', '*']]] = Argument(
                 None, help="Managers list. Use 'remove *' for removing all managers")):
    config = Config()
    data = set(config['managers'])
    if action is None:
        print(', '.join(data))
        sys.exit(0)
    match action:
        case 'add':
            for arg in args: data.add(arg)
        case 'remove':
            if '*' in args: data = set()
            else:
                for arg in args:
                    try: data.remove(arg)
                    except KeyError: pass
        case 'set': data = set(args)
        case _: raise ValueError('Invalid action')
    config['managers'] = set(data)


@app.command
def sync(hrenpack_only: bool = Option(False, '--hrenpack-only', '-H', 'o', help="Pull origin hrenpack only")):
    config = Config()
    code = 0
    if not hrenpack_only:
        code = os.system('git pull origin')
    if code == 0:
        os.chdir(config['directory'])
        code = os.system('git pull origin')
        os.chdir('..')
    for manager in config['managers']:
        if code != 0: break
        elif manager == 'uv': code = os.system(f'{manager} sync')
        elif manager in ('pipenv', 'npm', 'yarn'): code = os.system(f'{manager} install')
    sys.exit(code)


@app.command
def commit(hrenpack_only: bool = Option(False, '--hrenpack-only', '-H', 'o', help="Commit hrenpack only")):
    sys.exit(commands.commit(hrenpack_only))


@app.command
def push(hrenpack_only: bool = Option(False, '--hrenpack-only', '-H', 'o', help="Push origin hrenpack only"),
         commit_: bool = Option(False, '--commit', '-c', '-C', help="Commit hrenpack only")):
    if commit_:
        code = commands.commit(hrenpack_only)
        if code != 0: sys.exit(code)
    sys.exit(commands.push(hrenpack_only))


if __name__ == '__main__': app()
