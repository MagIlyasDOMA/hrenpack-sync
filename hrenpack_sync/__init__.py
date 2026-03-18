import os, sys
from typing import List, Optional
from typer import Typer, Argument, Option
from . import commands
from .json_config import Config

app = Typer(no_args_is_help=True)

VALID_MANAGERS = ['uv', 'pipenv', 'npm', 'yarn', '*']  # Определяем допустимые значения


@app.command
def clone(directory: str = Argument('hrenpack_source', help="Directory to clone")):
    config = Config()
    config['directory'] = directory
    sys.exit(os.system(f'git clone https://github.com/MagIlyasDOMA/hrenpack.git {directory}'))


@app.command
def managers(
        action: Optional[str] = Argument(None, help="Action to perform (add/remove/set)"),
        args: Optional[List[str]] = Argument(None, help="Managers list. Use 'remove *' for removing all managers")
):
    """Manage package managers configuration"""
    config = Config()
    data = set(config['managers'])

    # Показываем текущие менеджеры если action не указан
    if action is None:
        print(', '.join(data))
        sys.exit(0)

    # Валидация action
    if action not in ['add', 'remove', 'set']:
        print(f"Error: Invalid action '{action}'. Use add, remove, or set", file=sys.stderr)
        sys.exit(1)

    # Валидация args
    if args is None:
        args = []

    # Валидация значений менеджеров
    for arg in args:
        if arg not in VALID_MANAGERS:
            print(f"Error: Invalid manager '{arg}'. Valid managers: {', '.join(VALID_MANAGERS)}", file=sys.stderr)
            sys.exit(1)

    # Выполнение действия
    if action == 'add':
        for arg in args:
            data.add(arg)
    elif action == 'remove':
        if '*' in args:
            data = set()
        else:
            for arg in args:
                data.discard(arg)  # discard не вызывает ошибку если элемент отсутствует
    elif action == 'set':
        data = set(args)

    # Сохраняем изменения
    config['managers'] = list(data)  # Преобразуем set в list для JSON
    print(f"Managers updated: {', '.join(data)}")


@app.command
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

    for manager in config['managers']:
        if code != 0:
            break
        elif manager == 'uv':
            code = os.system(f'{manager} sync')
        elif manager in ('pipenv', 'npm', 'yarn'):
            code = os.system(f'{manager} install')

    sys.exit(code)


@app.command
def commit(
        hrenpack_only: bool = Option(False, '--hrenpack-only', '-H', help="Commit hrenpack only")
):
    """Commit changes"""
    sys.exit(commands.commit(hrenpack_only))


@app.command
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