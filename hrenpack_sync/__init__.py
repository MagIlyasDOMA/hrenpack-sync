import os, sys
from typing import List, Optional
from typer import Typer, Argument, Option
from . import commands
from .json_config import Config
from .enum import Manager

app = Typer(no_args_is_help=True)

VALID_MANAGERS = ['uv', 'pipenv', 'npm', 'yarn', '*']


@app.command()
def clone(directory: str = Argument('hrenpack_source', help="Directory to clone"),
          dry_run: bool = Option(False, '--dry-run', '--not-clone', '-d', '-c')):
    """Clone the hrenpack repository"""
    config = Config()
    config['directory'] = directory
    if not dry_run:
        sys.exit(os.system(f'git clone https://github.com/MagIlyasDOMA/hrenpack.git {directory}'))
    else: sys.exit(0)


@app.command
def managers(
    action: Optional[str] = Argument(None, help="Action to perform (add/remove/set)"),
    args: Optional[List[Manager]] = Argument(None, help="Managers list. Use 'remove *' for removing all managers")
):
    config = Config()
    data = set(config['managers'])

    if action is None:
        print(', '.join(data))
        sys.exit(0)

    if args is None:
        args = []

    # Конвертируем Enum в строки
    str_args = [m.value for m in args]

    if action == 'add':
        for arg in str_args:
            data.add(arg)
    elif action == 'remove':
        if Manager.ALL.value in str_args:
            data = set()
        else:
            for arg in str_args:
                data.discard(arg)
    elif action == 'set':
        data = set(str_args)
    else:
        print(f"Error: Invalid action '{action}'")
        sys.exit(1)

    config['managers'] = list(data)


@app.command()
def sync(
        hrenpack_only: bool = Option(False, '--hrenpack-only', '-H', help="Pull origin hrenpack only")
):
    """Sync repositories and install dependencies"""
    config = Config()
    code = 0

    if not hrenpack_only:
        code = os.system('git pull origin')

    if code == 0:
        os.chdir(config['directory'])
        code = os.system('git pull origin')
        os.chdir('..')

    for manager in config.get('managers', []):
        if code != 0:
            break
        elif manager == 'uv':
            code = os.system(f'{manager} sync')
        elif manager in ('pipenv', 'npm', 'yarn'):
            code = os.system(f'{manager} install')

    sys.exit(code)


@app.command()
def commit(
        hrenpack_only: bool = Option(False, '--hrenpack-only', '-H', help="Commit hrenpack only")
):
    """Commit changes"""
    sys.exit(commands.commit(hrenpack_only))


@app.command()
def push(
        hrenpack_only: bool = Option(False, '--hrenpack-only', '-H', help="Push origin hrenpack only"),
        commit: bool = Option(False, '--commit', '-c', help="Commit before pushing")
):
    """Push changes"""
    if commit:
        code = commands.commit(hrenpack_only)
        if code != 0:
            sys.exit(code)
    sys.exit(commands.push(hrenpack_only))


if __name__ == '__main__':
    app()