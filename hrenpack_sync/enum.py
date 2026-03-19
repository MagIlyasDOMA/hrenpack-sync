from enum import Enum


class Manager(str, Enum):
    UV = "uv"
    PIPENV = "pipenv"
    NPM = "npm"
    YARN = "yarn"
    ALL = "*"
