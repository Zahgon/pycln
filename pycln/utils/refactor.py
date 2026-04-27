"""Pycln code refactoring utility."""

import ast
import os
import sys
from collections.abc import Iterable
from importlib import import_module
from typing import Optional, Union, cast

from .. import ISWIN
from . import iou, pathu, regexu, scan
from ._exceptions import (
    InitFileDoesNotExistError,
    ReadPermissionError,
    UnexpandableImportStar,
    UnparsableFile,
    UnsupportedCase,
    WritePermissionError,
    libcst_parser_syntax_error_message,
)
from ._nodes import Import, ImportFrom, NodeLocation
from .config import Config
from .report import Report

if sys.version_info < (3, 12):
    from pathlib import Path, _posix_flavour, _windows_flavour

    _flavour = _windows_flavour if ISWIN else _posix_flavour
else:
    from pathlib import Path

    _flavour = os.path

# Constants.
NOPYCLN = "nopycln"
CHANGE_MARK = "\n_CHANGED_"
TRANSFORM = ".transform"
PYCLN_UTILS = "pycln.utils"


class PyPath(Path):
    """Path subclass that has `is_stub` property."""

    _flavour = _flavour

    def __init__(self, *args) -> None:  # pylint: disable=unused-argument
        if sys.version_info < (3, 12):
            super().__init__()  # Path.__init__ does not take any args.
        else:
            super().__init__(*args)
        self._is_stub = regexu.is_stub_file(self)

    @property
    def is_stub(self) -> bool:
        pass


class LazyLibCSTLoader:
    """`transform.py` takes about '0.3s' to be loaded because of LibCST,
    therefore I've created this class to load it only if necessary.

    THIS CLASS DOES NOT INCLUDED ON THE TESTS SUITE. SO DON'T MODIFY IT
    FOR ANY REASON!
    """

    def __init__(self):
        self._module = None

    def __getattr__(self, name):
        if self._module is None:
            self._module = import_module(TRANSFORM, PYCLN_UTILS)
        return getattr(self._module, name)


transform = LazyLibCSTLoader()


class Refactor:
    """Refactor the given source.

    >>> refactor = Refactor(
    ...     configs,  # Should be created on the main function.
    ...     reporter,  # Should be created on the main function.
    ... )
    >>> file_path = "./source.py"
    >>> refactor.session(file_path)

    :param configs: `config.Config` instance.
    :param reporter: `report.Report` instance.
    """

    def __init__(self, configs: Config, reporter: Report):
        self.configs = configs
        self.reporter = reporter
        # Resetables.
        self._import_stats = scan.ImportStats(set(), set())
        self._source_stats = scan.SourceStats(set(), set(), set())
        self._path = PyPath("")
        self._is_init_without_all = False

    def _reset(self) -> None:
        pass

    @staticmethod
    def remove_useless_passes(source_lines: list[str]) -> list[str]:
        """Remove any useless `pass`.

        :param source_lines: source code lines.
        :returns: clean source code lines.
        """

        def remove_from_children(
            parent: ast.AST, children: Iterable, body_len: int, wl: set[ast.AST]
        ):
            pass

        pass

    def session(self, path: Path) -> None:
        """Refactoring session.

        Refactor the given `path` source code.

        :param path: `.py` file to refactor.
        """
        pass

    def _code_session(self, source_code: str) -> str:
        """Refactor the given `source_code`.

        :param source_code: python source code.
        :returns: fixed source code.
        """
        pass

    def _output(
        self,
        fixed_lines: list[str],
        original_lines: list[str],
        encoding: str,
        newline: str,
    ) -> None:
        """Output the given `fixed_lines`.

        :param fixed_lines: the refactored source lines.
        :param original_lines: unmodified source lines.
        :param encoding: file encoding.
        :param newline: original file newline (CRFL | FL).
        """
        pass

    def _analyze(self, tree: ast.AST) -> tuple[scan.SourceStats, scan.ImportStats]:
        """Analyze the given `tree`.

        :param tree: a parsed `ast.AST`.
        :returns: tuple of `ImportStats`, `SourceStats` and set of names to skip.
        """
        pass

    def _refactor(self, original_lines: list[str]) -> str:
        """Remove all unused imports from given `original_lines`.

        :param original_lines: unmodified lines.
        :reutrns: fixed source code.
        """
        pass

    def _get_used_names(
        self, node: Union[Import, ImportFrom], is_star: bool
    ) -> set[str]:
        """Get set of used names base on given `node` and `self._source_stats`.

        :param node: import node to names check.
        :param is_star: is '*' import node.
        :returns: set of used names.
        """
        pass

    def _transform(
        self,
        location: NodeLocation,
        used_names: set[str],
        original_lines: list[str],
        updated_lines: list[str],
    ) -> list[str]:
        """Rebuild and replace the import without any unused part.

        :param location: `node.location`.
        :param used_names: set of all used names.
        :param original_lines: file original code lines.
        :param updated_lines: code lines to modify.
        :returns: modified source lines (fixed lines).
        """
        pass

    def _expand_import_star(
        self, node: ImportFrom
    ) -> tuple[ImportFrom, Optional[bool]]:
        """Expand import star statement, `scan.expand_import_star` abstraction.

        :param node: `ImportFrom` that has a '*' as `alias.name`.
        :returns: expanded '*' import or the original node and True if it's star import.
        """
        pass

    def _is_partially_used(self, alias: ast.alias, is_star: bool) -> bool:
        """Determine if the alias name partially used or not.

        :param alias: an `ast.alias` node.
        :param is_star: is it a '*' import.
        :returns: whather the alias name partially used or not.
        """
        pass

    def _should_remove(
        self, node: Union[Import, ImportFrom], alias: ast.alias, is_star: bool
    ) -> bool:
        """Check if the alias should be removed or not.

        :param node: an `Import` or `ImportFrom`.
        :param alias: an `ast.alias` node.
        :param is_star: is it a '*' import.
        :returns: True if the alias should be removed else False.
        """
        pass

    def _has_used(self, name: str, is_star: bool) -> bool:
        """Check if the given import name has used.

        :param name: a name to check.
        :param is_star: is it a '*' import.
        :returns: True if the name has used else False.
        """
        pass

    def _has_side_effects(  # pylint: disable=dangerous-default-value
        self, module: str, node: Union[Import, ImportFrom], *, cache: dict = {}
    ) -> scan.HasSideEffects:
        """Check if the given import file tree has side effects.

        :param module: `alias.name` to check.
        :param node: an `ast.Import` or `ast.ImportFrom` node.
        :returns: side effects status.
        """
        pass

    @staticmethod
    def _insert(
        rebuilt_import: list[str],
        updated_lines: list[str],
        location: NodeLocation,
    ) -> list[str]:
        """Insert (replace) rebuilt import statement into `updated_lines`.

        :param rebuilt_import: an import statement ot insert.
        :param updated_lines: a list of source lines to modify.
        :param location: unmodified node location.
        :returns: fixed list of lines.
        """
        pass
