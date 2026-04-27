"""Pycln CST transforming utility."""

from pathlib import Path
from typing import Optional, TypeVar, Union, cast

import libcst as cst

from ._exceptions import UnsupportedCase
from ._nodes import NodeLocation

# Constants.
SPACE4 = " " * 4

# Custom types & annotations.
ImportT = TypeVar("ImportT", bound=Union[cst.Import, cst.ImportFrom])
TrailingCommaA = Union[cst.MaybeSentinel, cst.Comma]


class ImportTransformer(cst.CSTTransformer):
    """Import statements transformer.

    :param used_names: set of all used names to keep.
    :param location: `NodeLocation`.
    """

    def __init__(self, used_names: set[str], location: NodeLocation):
        if not used_names:
            # Bad class usage.
            raise ValueError("'used_names' parameter can't be empty set.")
        self._used_names = used_names
        self._location = location
        self._indentation = " " * (location.start.col or 0)

        # Style preservation.
        self._lpar: cst.LeftParen = self._multiline_lpar()
        self._rpar: cst.RightParen = self._multiline_rpar()
        self._trailing_comma: TrailingCommaA = cst.MaybeSentinel.DEFAULT

    def refactor_import_star(self, updated_node: cst.ImportFrom) -> cst.ImportFrom:
        """Add used import aliases to import star.

        :param updated_node: `cst.ImportFrom` node to refactor.
        :returns: refactored node.
        """
        pass

    def refactor_import(self, updated_node: ImportT) -> ImportT:
        """Remove unused imports from the given `updated_node`.

        :param updated_node: `cst.Import` or `cst.ImportFrom` node to refactor.
        :returns: refactored node.
        """
        pass

    def leave_Import(  # pylint: disable=W0613
        self, original_node: cst.Import, updated_node: cst.Import
    ) -> Optional[cst.Import]:
        pass

    def leave_ImportFrom(  # pylint: disable=W0613
        self, original_node: cst.ImportFrom, updated_node: cst.ImportFrom
    ) -> Optional[cst.ImportFrom]:
        pass

    def _set_lpar(self, node: cst.ImportFrom):
        # Set `self._lpar` base on the original node.
        pass

    def _set_rpar(self, node: cst.ImportFrom):
        # Set `self._rpar` base on the original node.
        pass

    def _set_trailing_comma(self, node: ImportT):
        # Set `self._trailing_comma` base on the original node.
        pass

    def _get_alias_name(
        self, node: Optional[Union[cst.Name, cst.Attribute]], name=""
    ) -> str:
        # Recursion function that calculates `node` string dotted name.
        pass

    @staticmethod
    def _multiline_parenthesized_whitespace(indent: str) -> cst.ParenthesizedWhitespace:
        # Return multiline parenthesized white space.
        pass

    def _multiline_alias(self, alias: cst.ImportAlias) -> cst.ImportAlias:
        # Convert the given `alias` to multiline `alias`.
        pass

    def _multiline_lpar(self) -> cst.LeftParen:
        # Return multiline `cst.LeftParen`.
        pass

    def _multiline_rpar(self) -> cst.RightParen:
        # Return multiline `cst.RightParen`.
        pass

    def _stylize(
        self,
        node: ImportT,
        used_aliases: list[cst.ImportAlias],
        force_multiline: bool = False,
    ) -> ImportT:
        # (Preserving `node` style).

        # Set the trailing comma determined by `_set_trailing_comma`.
        pass


def rebuild_import(
    import_stmnt: str,
    used_names: set[str],
    path: Path,
    location: NodeLocation,
) -> list[str]:
    """Rebuild the given `import_stmnt` based on `used_names` using `LibCST`.

    :param import_stmnt: source code of the import statement.
    :param used_names: set of all used names to keep.
    :param path: where `import_stats` has imported.
    :param location: `NodeLocation`.
    :returns: fixed import statement source code as list of lines.
    :raises cst.ParserSyntaxError: in some rare cases.
    :raises UnsupportedCase: in some rare cases.
    """
    pass
