"""Pycln regex utility."""

import os
import re
import tokenize
from pathlib import Path
from re import Pattern

import typer
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern

from .. import ISWIN

# Constants.
INCLUDE = "include"
EXCLUDE = "exclude"
GITIGNORE = ".gitignore"
SKIP_FILE_REGEX = r"# *(nopycln *: *file).*"
SKIP_IMPORT_REGEX = r"# *((noqa *:*)|(nopycln *: *import)).*"
INIT_FILE_REGEX = r"^__init__.pyi?$"
STUB_FILE_REGEX = r".*\.pyi$"
EMPTY_REGEX = r"^$"
INCLUDE_REGEX = r".*\.pyi?$"
EXCLUDE_REGEX = (
    r"(\.eggs|\.git|\.hg|\.mypy_cache|__pycache__|\.nox|"
    + r"\.tox|\.venv|\.svn|buck-out|build|dist)/"
)


def safe_compile(pattern: str, type_: str) -> Pattern[str]:
    """Safely compile [--include, --exclude] options regex.

    :param pattern: an str regex to be complied.
    :param type_: 'include' OR 'exclude'.
    :returns: complied regex.
    """
    pass


def strpath(path: Path) -> str:
    """Custom `Path` to `str` casting.

    :param path: file-system path.
    :returns: stringified path.
    """
    pass


def is_init_file(path: Path) -> bool:
    """Check if the file name is `__init__.py(i)`.

    :param path: file-system path to check.
    :returns: True if the file is `__init__.py(i)` else False.
    """
    pass


def is_stub_file(path: Path) -> bool:
    """Check if the file extension is `.pyi`.

    :param path: file-system path to check.
    :returns: True if the file extension is `.pyi` else False.
    """
    pass


def is_included(path: Path, regex: Pattern[str]) -> bool:
    """Check if the file/directory name match include pattern.

    :param path: file-system path to check.
    :param regex: include regex pattern.
    :returns: True if the name match else False.
    """
    pass


def is_excluded(path: Path, regex: Pattern[str]) -> bool:
    """Check if the file/directory name match exclude pattern.

    :param path: file-system path to check.
    :param regex: exclude regex pattern.
    :returns: True if the name match else False.
    """
    pass


def get_gitignore(root: Path, no_gitignore: bool = False) -> PathSpec:
    """Return a PathSpec matching gitignore content, if present.

    :param root: root path to search for `.gitignore`.
    :param no_gitignore: `config.no_gitignore` value (default=False).
    :returns: PathSpec matching gitignore content, if present.
    """
    pass


def skip_import(line: str) -> bool:
    """Check if the lines has `# noqa` or `# nopycln: import` to skip.

    :param line: a line to check.
    :returns: True if it matches else False.
    """
    pass


def skip_file(src_code: str) -> bool:
    """Check if the src_code code has `nopycln: file` comment to skip.

    :param src_code: string source code to check.
    :returns: True if it matches else False.
    """
    pass
