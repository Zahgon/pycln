"""Pycln source code AST analysis utility."""

import ast
import os
from dataclasses import dataclass
from enum import Enum, unique
from functools import wraps
from pathlib import Path
from typing import Any, Callable, TypeVar, Union, cast

from . import _nodes, iou, pathu
from ._exceptions import ReadPermissionError, UnexpandableImportStar, UnparsableFile

# Constants.
__ALL__ = "__all__"
NAMES_TO_SKIP = frozenset(
    {
        "__name__",
        "__doc__",
        "__package__",
        "__loader__",
        "__spec__",
        "__build_class__",
        "__import__",
        __ALL__,
    }
)
SUBSCRIPT_TYPE_VARIABLE = frozenset(
    {
        "AbstractSet",
        "AsyncContextManager",
        "AsyncGenerator",
        "AsyncIterable",
        "AsyncIterator",
        "Awaitable",
        "ByteString",
        "Callable",
        "ChainMap",
        "ClassVar",
        "Collection",
        "Container",
        "ContextManager",
        "Coroutine",
        "Counter",
        "DefaultDict",
        "Deque",
        "Dict",
        "FrozenSet",
        "Generator",
        "IO",
        "ItemsView",
        "Iterable",
        "Iterator",
        "KeysView",
        "List",
        "Mapping",
        "MappingView",
        "Match",
        "MutableMapping",
        "MutableSequence",
        "MutableSet",
        "Optional",
        "Pattern",
        "Reversible",
        "Sequence",
        "Set",
        "SupportsRound",
        "Tuple",
        "Type",
        "Union",
        "ValuesView",
        # Python >=3.7:
        "Literal",
        # Python >=3.8:
        "OrderedDict",
        # Python >=3.9:
        "tuple",
        "list",
        "dict",
        "set",
        "frozenset",
        "type",
    }
)

# Custom types.
FunctionT = TypeVar("FunctionT", bound=Callable[..., Any])
FunctionDefT = TypeVar(
    "FunctionDefT", bound=Union[ast.FunctionDef, ast.AsyncFunctionDef]
)


def recursive(func: FunctionT) -> FunctionT:
    """decorator to make `ast.NodeVisitor` work recursive.

    :param func: `ast.NodeVisitor.visit_*` function.
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        pass

    pass


@dataclass
class ImportStats:
    """Import statements statistics."""

    import_: set[_nodes.Import]
    from_: set[_nodes.ImportFrom]

    def __iter__(self):
        return iter([self.import_, self.from_])


@dataclass
class SourceStats:
    """Source code (`ast.Name`, `ast.Attribute`) statistics."""

    #: Included on `__iter__`.
    name_: set[str]
    attr_: set[str]

    #: Not included on `__iter__`.
    names_to_skip: set[str]

    def __iter__(self):
        return iter([self.name_, self.attr_])


class SourceAnalyzer(ast.NodeVisitor):
    """AST source code analyzer.

    >>> import ast
    >>> source = "source.py"
    >>> with open(source, "r") as sourcef:
    >>>     source_lines = sourcef.readlines()
    >>>     tree = ast.parse("".join(source_lines))
    >>> analyzer = SourceAnalyzer()
    >>> analyzer.visit(tree)
    >>> source_stats, import_stats = analyzer.get_stats()
    """

    def __init__(self):
        self._has_all = False  # True if the source has an `__all__` dunder.
        self._import_stats = ImportStats(set(), set())
        self._imports_to_skip: set[Union[_nodes.Import, _nodes.ImportFrom]] = set()
        self._source_stats = SourceStats(set(), set(), set())

    @recursive
    def visit_Import(self, node: ast.Import):
        pass

    @recursive
    def visit_ImportFrom(self, node: ast.ImportFrom):
        pass

    @recursive
    def visit_Name(self, node: ast.Name):
        pass

    @recursive
    def visit_Attribute(self, node: ast.Attribute):
        pass

    @recursive
    def visit_MatchAs(self, node: "ast.MatchAs"):
        #: Support Match statement (PYTHON >= 3.10).
        #: PEP0634: https://www.python.org/dev/peps/pep-0634/
        pass

    @recursive
    def visit_Call(self, node: ast.Call):
        pass

    @recursive
    def visit_Subscript(self, node: ast.Subscript) -> None:
        #: Support semi string type assigment
        #:
        #: >>> from ast import Import, ImportFrom
        #: >>> from typing import Union, List
        #: >>>
        #: >>> bar = List['Import']
        #: >>> foo = Union['Import', 'ImportFrom']
        pass

    @recursive
    def visit_AnnAssign(self, node: ast.AnnAssign):
        #: Support all
        #:
        #: 1) string type annotations:
        #:  >>> foo: "Bar[Baz]" = []
        #:
        #: 2) nested string type annotations:
        #:  >>> bar: "Bar['Baz']" = []
        #:
        #: 3) semi string type annotations:
        #:  >>> foo: Bar["Baz"] = []
        pass

    @recursive
    def visit_arg(self, node: ast.arg):
        # Support Python ^3.8 type comments.
        pass

    @recursive
    def visit_FunctionDef(self, node: FunctionDefT):
        # Support Python ^3.8 type comments.
        pass

    # Support `ast.AsyncFunctionDef`.
    visit_AsyncFunctionDef = visit_FunctionDef

    @recursive
    def visit_ClassDef(self, node: ast.ClassDef):
        #: Support imports used in generics and wrapped in string:
        #:
        #: >>> from typing import Generic
        #: >>> from foo import Bar
        #: >>>
        #: >>> class SuperClass(Generic[SomeType]):
        #: >>>     ...
        #: >>>
        #: >>> class SubClass(SuperClass["Bar"])  # <~ detecting Bar.
        #: >>>     ...
        #:
        #: Issue: https://github.com/hadialqattan/pycln/issues/169
        pass

    @recursive
    def visit_Assign(self, node: ast.Assign):
        # Support Python ^3.8 type comments.
        pass

    @recursive
    def visit_AugAssign(self, node: ast.AugAssign):
        pass

    @recursive
    def visit_Expr(self, node: ast.Expr):
        #: Support `__all__` dunder overriding with
        #: `append` and `extend` operations:
        #:
        #: >>> import x, y, z
        #: >>>
        #: >>> __all__ = ["x"]
        #: >>> __all__.append("y")
        #: >>> __all__.extend(["z"])
        #:
        #: Issue: https://github.com/hadialqattan/pycln/issues/29
        pass

    def _visit_string_type_annotation(
        self, node: Union[ast.AnnAssign, ast.arg, FunctionDefT]
    ) -> None:
        # Support string type annotations.
        pass

    def _visit_type_comment(
        self, node: Union[ast.Assign, ast.arg, FunctionDefT]
    ) -> None:
        #: Support Python ^3.8 type comments.
        #:
        #: This feature is only available for Python ^3.8.
        #: PEP 526 -- Syntax for Variable Annotations.
        #: For more information:
        #:     - https://www.python.org/dev/peps/pep-0526/
        #:     - https://docs.python.org/3.8/library/ast.html#ast.parse
        pass

    def _parse_string(
        self, node: ast.Constant, is_str_annotation: bool = False
    ) -> None:
        pass

    def _add_concatenated_list_names(self, node: ast.BinOp) -> None:
        #: Safely add `["x", "y"] + ["i", "j"]`
        #: `const/str` names to `self._source_stats.name_`.
        pass

    def _add_list_names(self, node: list[ast.expr]) -> None:
        # Safely add list `const/str` names to `self._source_stats.name_`.
        pass

    def _add_name_attr_const(self, tree: ast.AST, is_str_annotation: bool = False):
        # Add any `ast.Name`, `ast.Attribute`, and (`ast.Constant` if is_str_annotation)
        # child to `self._source_stats`.
        pass

    def _get_import_node(self, node: ast.Import) -> _nodes.Import:
        pass

    def _get_import_from_node(self, node: ast.ImportFrom) -> _nodes.ImportFrom:
        pass

    def get_stats(self) -> tuple[SourceStats, ImportStats]:
        """Get source analyzer results.

        :returns: tuple of `SourceStats` and `ImportStats`.
        """
        pass

    def has_all(self) -> bool:
        """`self._has_all` getter.

        :returns: True if the source includes an `__all__` dunder.
        """
        pass


class ImportablesAnalyzer(ast.NodeVisitor):
    """Get set of all importable names from given `ast.Module`.

    >>> import ast
    >>> source = "source.py"
    >>> with open(source, "r") as sourcef:
    >>>     tree = ast.parse(sourcef.read())
    >>> analyzer = ImportablesAnalyzer(source)
    >>> analyzer.visit(tree)
    >>> importable_names = analyzer.get_stats()

    :param path: a file path that belongs to the given `ast.Module`.
    """

    def __init__(self, path: Path):
        self._not_importables: set[Union[ast.Name, str]] = set()
        self._importables: set[str] = set()
        self._has_all = False  # True if the source has an `__all__` dunder.
        self._path = path

    @recursive
    def visit_Assign(self, node: ast.Assign):
        pass

    @recursive
    def visit_AugAssign(self, node: ast.AugAssign):
        pass

    @recursive
    def visit_Expr(self, node: ast.Expr):
        #: Support `__all__` dunder overriding with
        #: `append` and `extend` operations:
        #:
        #: >>> import x, y, z
        #: >>>
        #: >>> __all__ = ["x"]
        #: >>> __all__.append("y")
        #: >>> __all__.extend(["z"])
        #:
        #: Issue: https://github.com/hadialqattan/pycln/issues/29
        pass

    @recursive
    def visit_Import(self, node: ast.Import):
        # Analyze each import statement.
        pass

    @recursive
    def visit_ImportFrom(self, node: ast.ImportFrom):
        # Analyze each importFrom statement.
        pass

    @recursive
    def visit_FunctionDef(self, node: FunctionDefT):
        # Add function name as importable name.
        pass

    # Support `ast.AsyncFunctionDef`.
    visit_AsyncFunctionDef = visit_FunctionDef

    @recursive
    def visit_ClassDef(self, node: ast.ClassDef):
        # Add class name as importable name.
        pass

    @recursive
    def visit_Name(self, node: ast.Name):
        pass

    def _add_concatenated_list_names(self, node: ast.BinOp) -> None:
        #: Safely add `["x", "y"] + ["i", "j"]`
        #: `const/str` names to `self._importables`.
        pass

    def _add_list_names(self, node: list[ast.expr]) -> None:
        # Safely add list `const/str` names to `self._importables`.
        pass

    def _compute_not_importables(self, node: Union[FunctionDefT, ast.ClassDef]):
        # Compute class/function not-importables.
        pass

    def get_stats(self) -> set[str]:
        pass

    def generic_visit(self, node):
        """Called if no explicit visitor function exists for a node
        (override)."""
        pass


@unique
class HasSideEffects(Enum):
    """SideEffects values."""

    YES = 1
    MAYBE = 0.5
    NO = 0

    #: Some names aren't modules.
    NOT_MODULE = -1

    #: Just in case an exception has raised
    #: while parsing a file.
    NOT_KNOWN = -2


class SideEffectsAnalyzer(ast.NodeVisitor):
    """Check if the given `ast.Module` has side effects or not.

    >>> import ast
    >>> source = "source.py"
    >>> with open(source, "r") as sourcef:
    >>>     tree = ast.parse(sourcef.read())
    >>> analyzer = SideEffectsAnalyzer()
    >>> analyzer.visit(tree)
    >>> has_side_effects = analyzer.has_side_effects()
    """

    def __init__(self):
        self._not_side_effects: set[ast.Call] = set()
        self._has_side_effects = HasSideEffects.NO

    @recursive
    def visit_FunctionDef(self, node: FunctionDefT):
        # Mark any call inside a function as not-side-effect.
        pass

    # Support `ast.AsyncFunctionDef`.
    visit_AsyncFunctionDef = visit_FunctionDef

    @recursive
    def visit_ClassDef(self, node: ast.ClassDef):
        # Mark any call inside a class as not-side-effect.
        pass

    def _compute_not_side_effects(
        self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef]
    ) -> None:
        # Mark any call inside the given `node` as not-side-effect.
        pass

    @recursive
    def visit_Call(self, node: ast.Call):
        pass

    @recursive
    def visit_Import(self, node: ast.Import):
        pass

    @recursive
    def visit_ImportFrom(self, node: ast.ImportFrom):
        pass

    @staticmethod
    def _check_names(names: list[ast.alias]) -> HasSideEffects:
        # Check if imported names has side effects or not.
        pass

    def has_side_effects(self) -> HasSideEffects:
        pass

    def generic_visit(self, node):
        """Called if no explicit visitor function exists for a node
        (override)."""
        pass


def expand_import_star(
    node: Union[ast.ImportFrom, _nodes.ImportFrom], path: Path
) -> Union[ast.ImportFrom, _nodes.ImportFrom]:
    """Expand import star statement, replace the `*` with a list of ast.alias.

    :param node: `_nodes/ast.ImportFrom` node that has a '*' as `alias.name`.
    :param path: where the node has imported.
    :returns: expanded `_nodes/ast.ImportFrom` (same input node type).
    :raises UnexpandableImportStar: when `ReadPermissionError`,
        `UnparsableFile` or `ModuleNotFoundError` or `RecursionError` raised.
    """
    pass


def parse_ast(source_code: str, path: Path = Path(""), mode: str = "exec") -> ast.AST:
    """Parse the given `source_code` AST.

    :param source_code: python source code.
    :param path: `source_code` file path.
    :param mode: `ast.parse` mode.
    :returns: `ast.AST` (source code AST).
    :raises UnparsableFile: if the compiled source is invalid,
        or the source contains null bytes.
    """
    pass
