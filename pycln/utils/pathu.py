"""Pycln path finding utility."""

import os
import sys
import sysconfig
from collections.abc import Generator
from functools import lru_cache
from pathlib import Path
from re import Pattern
from typing import Optional

from pathspec import PathSpec

from vendor.custom import _site

from .. import ISWIN
from . import regexu
from .report import Report

# Constants.
EXCLUDE = "exclude"
INCLUDE = "include"
GITIGNORE = "gitignore"
PY_EXTENSION = ".py"
PTH_EXTENSION = ".pth"
__INIT__ = "__init__.py"
LIB_DYNLOAD = "Lib" if ISWIN else "lib-dynload"
SITE_PACKAGES = "site-packages"
DIST_PACKAGES = "dist-packages"
LIB_PY_EXTENSIONS = ("so", "py", "pyc")
BIN_PY_EXTENSIONS = ("so", "egg-info", "nspkg.pth")
BIN_IMPORTS = {  # In case they are built into CPython.
    "io",
    "os",
    "sys",
    "grp",
    "pwd",
    "json",
    "math",
    "time",
    "parser",
    "string",
    "operator",
    "datetime",
    "multiprocessing",
}
IMPORTS_WITH_SIDE_EFFECTS = {"this", "antigravity", "rlcompleter"}
PYTHON_STDLIB_PATHS = frozenset(
    {sysconfig.get_path("platstdlib"), sysconfig.get_path("stdlib")}
)


def yield_sources(
    path: Path,
    include: Pattern[str],
    exclude: Pattern[str],
    extend_exclude: Pattern[str],
    gitignore: PathSpec,
    reporter: Report,
) -> Generator[Path, None, None]:
    """Yields `.py` and `.pyi` paths to handle. Walk throw path sub-
    directories/files recursively.

    :param path: A path to start searching from.
    :param include: regex pattern to be included.
    :param exclude: regex pattern to be excluded.
    :param extend_exclude: regex pattern to be excluded in addition to `exclude`.
    :param gitignore: gitignore PathSpec object.
    :param reporter: a `report.Report` object.
    :returns: generator of `.py` and `.pyi` files paths.
    """
    pass


@lru_cache
def get_standard_lib_paths() -> set[Path]:
    """Get paths to Python standard library modules.

    :returns: set of paths to Python standard library modules.
    """
    pass


@lru_cache
def get_standard_lib_names() -> set[str]:
    """Returns a set of Python standard library modules names.

    :returns: a set of Python standard library modules names.
    """
    pass


@lru_cache
def get_third_party_lib_paths() -> tuple[set[Path], set[Path]]:
    """Get paths to third party library modules.

    :returns: a tuple of a set of paths of third party library modules
        and a set of paths from `.pth` file(s) content, respectively.
    """
    pass


@lru_cache
def get_local_import_path(path: Path, module: str) -> Optional[Path]:
    """Find the given local module file.py/__init_.py path.

    Written FOR `ast.Import`.

    :param path: where `module` has imported.
    :param module: a module name.
    :returns: a full `module/__init__.py` path.
    """
    pass


def get_local_import_pth_path(pth_paths: set[Path], module: str) -> Optional[Path]:
    """Find the given local module file.py/__init__.py path base on the
    provided `pth_paths` set.

    :param pth_paths: a set of local paths read from a `.pth` file.
    :param module: a module name.
    :returns: a full `module/__init__.py` path.
    """
    pass


@lru_cache
def get_local_import_from_path(
    path: Path, module: str, package: str, level: int
) -> Optional[Path]:
    """Find the given local module file.py/__init_.py path.

    Written FOR `ast.ImportFrom`.

    :param path: where `module` has imported.
    :param module: a module name.
    :param package: a package name.
    :param level: `ast.ImportFrom.level`.
    :returns: a full `module/__init__.py` path.
    """
    pass


def get_local_import_from_pth_path(
    pth_paths: set[Path], module: str, package: str, level: int
) -> Optional[Path]:
    """Find the given local module file.py/__init__.py path base on the
    provided `pth_paths` set.

    Written FOR `ast.ImportFrom`.

    :param pth_paths: a set of local paths read from a `.pth` file.
    :param module: a module name.
    :param package: a package name.
    :param level: `ast.ImportFrom.level`.
    :returns: a full `module/__init__.py` path.
    """
    pass


def get_module_path(
    paths: set[Path], module: str, package: str = "", level: int = 0
) -> Optional[Path]:
    """Get the `module` path from the given `paths`.

    :param paths: a list of paths to search.
    :param module: a module name.
    :param package: a package name.
    :param level: `ast.ImportFrom.level`.
    :returns: `module` path if exist else None.
    """
    pass


@lru_cache
def get_import_path(path: Path, module: str) -> Optional[Path]:
    """Find the given module file.py/__init__.py path.

    Written for `ast.Import` nodes.

    :param path: where module has imported.
    :param module: module name.
    :returns: `module` file.py/__init_.py path, if found else None.
    """
    pass


@lru_cache
def get_import_from_path(
    path: Path, module: str, package: str, level: int
) -> Optional[Path]:
    """Find the given module file.py/__init_.py path.

    Written for `ast.ImportFrom` nodes.

    :param path: where module has imported.
    :param module: module name.
    :param package: package name.
    :param level: `ast.ImportFrom.level`.
    :returns: `module` file.py/__init_.py path, if found else None.
    """
    pass
