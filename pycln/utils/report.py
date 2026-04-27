"""Pycln report utility."""

import ast
from dataclasses import dataclass
from difflib import unified_diff
from pathlib import Path
from typing import Optional, Union

import typer

from . import _nodes, config


@dataclass
class Report:
    """Provide a Pycln report counters.

    Can be rendered with `str(report)`.
    """

    #: Configured instance.
    configs: config.Config

    @staticmethod
    def get_location(path: Path, location: _nodes.NodeLocation) -> str:
        """Create full location from `path` and node location.

        :param path: file path.
        :param location: `_nodes.NodeLocation`.
        :returns: full location.
        """
        pass

    @staticmethod
    def secho(
        message: str,
        *,  # Force kwargs.
        bold: bool,
        isedit: bool = False,
        issuccess: bool = False,
        iswarning: bool = False,
        iserror: bool = False,
    ) -> None:
        """Print a colored message.

        :param message: a string message.
        :param bold: is if a bold message.
        :param isedit: is it an edit message ~> stdout.
        :param issuccess: is it a success message  ~> stdout.
        :param iswarning: is it a warning message ~> stderr.
        :param iserror: is it an error message ~> stderr.
        """
        pass

    @staticmethod
    def colored_unified_diff(
        path: Path,
        original_lines: list[str],
        fixed_lines: list[str],
    ) -> None:
        """Writeout colored and normalized diff.

        :param path: a file path.
        :param original_lines: original source code lines.
        :param fixed_lines: fixed soruce code lines.
        """
        pass

    @staticmethod
    def output_stdin_to_stdout(fixed_lines: list[str]) -> None:
        """Printout the given fixed lines to STDOUT.

        :param fixed_lines: fixed soruce code lines.
        """
        pass

    @staticmethod
    def rebuild_report_import(
        node: Union[_nodes.Import, _nodes.ImportFrom],
        alias: ast.alias,
    ) -> str:
        """Rebuild import statement from AST for reporting purposes.

        :param node: import node.
        :param alias: `ast.alias` node.
        """
        pass

    #: Total removed import statements counter.
    _removed_imports: int = 0

    def removed_import(
        self,
        path: Path,
        node: Union[_nodes.Import, _nodes.ImportFrom],
        removed_alias: ast.alias,
    ) -> None:
        """Increment `self._removed_imports`. Write a message to stdout.

        :param path: where the import was removed.
        :param node: removed import node.
        :param removed_alias: the removed `ast.alias` from the node.
        """
        pass

    #: Total expanded import statements counter.
    _expanded_stars: int = 0

    def expanded_star(self, path: Path, node: _nodes.ImportFrom) -> None:
        """Increment `self._expanded_stars`. Write a message to stdout.

        :param path: where the import was expanded.
        :param node: the expanded node.
        """
        pass

    #: Total changed files counter.
    _changed_files: int = 0

    #: These counters will be reseted for each file.
    _file_removed_imports: int = 0
    _file_expanded_stars: int = 0

    def _reset_file_counters(self) -> None:
        pass

    def changed_file(self, path: Path) -> None:
        """Increment `self._changed_files`. Write a message to stdout.

        :param path: the changed file path.
        """
        pass

    #: Total unchanged files counter.
    _unchanged_files: int = 0

    def unchanged_file(self, path: Path) -> None:
        """Increment `self._unchanged_files`. Write a message to stdout.

        :param path: the unchanged file path.
        """
        pass

    #: Total ignored paths counter.
    _ignored_paths: int = 0

    def ignored_path(self, ignored_path: Path, type_: str) -> None:
        """Increment `self._ignored_paths`. Write a message to stderr.

        :param ignored_path: the ignored path.
        :param type_: ignore type (`exclude`, `include`, `gitignore` or `nopycln`).
        """
        pass

    #: Total ignored import statements counter.
    _ignored_imports: int = 0

    def ignored_import(
        self,
        path: Path,
        node: Union[_nodes.Import, _nodes.ImportFrom],
        is_star: bool = False,
    ) -> None:
        """Increment `self._ignored_imports`. Write a message to stderr.

        :param path: where the import was ignored.
        :param node: the ignored import node.
        :param is_star: set to true if it's a '*' import.
        """
        pass

    #: Total number of failures.
    _failures: int = 0

    def failure(self, msg: str, path: Optional[Path] = None) -> None:
        """Increment `self._failures`. Write a msg to stderr.

        :param msg: a failure msg.
        :param path: where the failure has appeared.
        """
        pass

    #: Total number of undecidable cases
    _undecidable_case: int = 0

    def init_without_all_warning(self, path: Path) -> None:
        """Increment `self._undecidable_case`. Write a msg to stderr.

        :param path: the `__init__.py` file path.
        """
        pass

    @property
    def exit_code(self) -> int:
        """Return an exit code.

        :returns: an exit code (0, 1, 250).
        """
        pass

    @property
    def report_prefix(self) -> str:
        """Return the correct prefix.

        :returns: `"\n"` or `""`.
        """
        pass

    def __str__(self) -> str:
        """Render a colored report of the current state.

        Use `typer.unstyle` to remove colors.

        :returns: a colored report of the current state.
        """
        if self.configs.silence:
            return ""

        if not any([self._changed_files, self._unchanged_files, self._failures]):
            typer.secho(
                ("\n" if self.configs.verbose and self._ignored_paths else "")
                + "No Python files are present to be cleaned. Nothing to do 😴",
                bold=True,
            )
            raise typer.Exit(0)

        if any([self.configs.check, self.configs.diff]):
            removed_imports = "would be removed"
            removed_imports_plural = removed_imports
            expanded_stars = "would be expanded"
            expanded_stars_plural = expanded_stars
            changed_files = "would be changed"
            changed_files_plural = changed_files
            unchanged_files = "would be left unchanged"
            unchanged_files_plural = unchanged_files
            undecidable_case = "would be skipped"
            undecidable_case_plural = undecidable_case
        else:
            removed_imports = "was removed"
            removed_imports_plural = "were removed"
            expanded_stars = "was expanded"
            expanded_stars_plural = "were expanded"
            changed_files = "was changed"
            changed_files_plural = "were changed"
            unchanged_files = "left unchanged"
            unchanged_files_plural = "left unchanged"
            undecidable_case = "was skipped"
            undecidable_case_plural = "were skipped"
        failures = "has failed to be cleaned"
        failures_plural = "have failed to be cleaned"

        report = []

        if self._removed_imports:
            plural = self._removed_imports > 1
            report.append(
                typer.style(
                    f"{self._removed_imports} import{'s' if plural else ''} "
                    f"{removed_imports_plural if plural else removed_imports}",
                    bold=True,
                )
            )

        if self._expanded_stars:
            plural = self._expanded_stars > 1
            report.append(
                typer.style(
                    f"{self._expanded_stars} import{'s' if plural else ''} "
                    f"{expanded_stars_plural if plural else expanded_stars}",
                    bold=True,
                )
            )

        if self._changed_files:
            plural = self._changed_files > 1
            report.append(
                typer.style(
                    f"{self._changed_files} file{'s' if plural else ''} "
                    f"{changed_files_plural if plural else changed_files}",
                    bold=True,
                )
            )

        if self._unchanged_files:
            plural = self._unchanged_files > 1
            report.append(
                typer.style(
                    f"{self._unchanged_files} file{'s' if plural else ''} "
                    f"{unchanged_files_plural if plural else unchanged_files}",
                    bold=False,
                )
            )

        if self._failures:
            plural = self._failures > 1
            report.append(
                typer.style(
                    f"{self._failures} file{'s' if plural else ''} "
                    f"{failures_plural if plural else failures}",
                    bold=False,
                )
            )

        if self._undecidable_case:
            plural = self._undecidable_case > 1
            report.append(
                typer.style(
                    f"{self._undecidable_case} undecidable case{'s' if plural else ''} "
                    f"{undecidable_case_plural if plural else undecidable_case}",
                    bold=False,
                )
            )

        if self.configs.verbose:
            ignored_imports = "was ignored"
            ignored_imports_plural = "were ignored"
            ignored_paths = "was ignored"
            ignored_paths_plural = "were ignored"

            if self._ignored_imports:
                plural = self._ignored_imports > 1
                report.append(
                    typer.style(
                        f"{self._ignored_imports} import{'s' if plural else ''} "
                        f"{ignored_imports_plural if plural else ignored_imports}",
                        bold=False,
                    )
                )

            if self._ignored_paths:
                plural = self._ignored_paths > 1
                report.append(
                    typer.style(
                        f"{self._ignored_paths} path{'s' if plural else ''} "
                        f"{ignored_paths_plural if plural else ignored_paths}",
                        bold=False,
                    )
                )

        if not self._failures:
            if self._undecidable_case:
                s = (
                    "were undecidable cases"
                    if self._undecidable_case > 1
                    else "was an undecidable case"
                )
                done_msg = f"Wait a minute, there {s}! 😳😅"
            elif self._removed_imports or self._expanded_stars:
                done_msg = "All done! 💪 😎"
            else:
                done_msg = "Looks good! ✨ 🍰 ✨"
        else:
            s = "were errors" if self._failures > 1 else "was an error"
            done_msg = f"Oh no, there {s}! 💔 ☹️"

        sdone_msg = typer.style(done_msg + "\n", bold=True)
        return self.report_prefix + sdone_msg + ", ".join(report) + ".\n"
