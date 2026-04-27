"""Pycln file IO utility."""

import io
import os
import sys
import tokenize
from pathlib import Path

from ._exceptions import (
    InitFileDoesNotExistError,
    ReadPermissionError,
    UnparsableFile,
    WritePermissionError,
)

# Constants.
STDIN_FILE = Path("STDIN")
STDIN_NOTATION = Path("-")
FORM_FEED_CHAR = "\x0c"
CRLF = "\r\n"
LF = "\n"
__INIT__ = "__init__.py"

# Types
FileContent = str
Encoding = str
NewLine = str


def read_stdin() -> tuple[FileContent, Encoding, NewLine]:
    """Read the content of STDIN with encoding and new line type detection.

    :returns: decoded source code, file encoding, and a newline.
    :raises UnparsableFile: If both a BOM and a cookie are present, but disagree.
        or some rare characters presented.
    """
    pass


def safe_read(
    path: Path, permissions: tuple = (os.R_OK, os.W_OK)
) -> tuple[FileContent, Encoding, NewLine]:
    """Read file content with encoding and new line type detection.

    :param path: `.py` file path.
    :returns: decoded source code, file encoding, and a newline.
    :raises ReadPermissionError: when `os.R_OK` in permissions
        and the source does not have read permission.
    :raises WritePermissionError: when `os.W_OK` in permissions
        and the source does not have write permission.
    :raises UnparsableFile: If both a BOM and a cookie are present, but disagree.
        or some rare characters presented.
    :raises InitFileDoesNotExistError: when `path` is a path to a non-existing
        `__init__.py` file.
    """
    pass


def safe_write(path: Path, fixed_lines: list[str], encoding: str, newline: str) -> None:
    """Write file content based on given `encoding`.

    :param path: `.py` file path.
    :param encoding: file encoding.
    :param fixed_lines: fixed source code lines.
    :param newline: output file's newline (CRFL | FL).
    :raises WritePermissionError: when `os.W_OK` in permissions
        and the source does not have write permission.
    """
    pass
