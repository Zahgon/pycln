"""Pycln configuration management utility."""

import configparser
import json
import tokenize
from dataclasses import dataclass
from pathlib import Path
from re import Pattern
from typing import Optional, Union

import tomlkit
import typer
import yaml

from . import iou, regexu

# Constants.
CONFIG_SECTIONS = {
    ".cfg": "pycln",
    ".toml": "tool.pycln",
    ".json": "pycln",
    ".yaml": "pycln",
    ".yml": "pycln",
}


@dataclass
class Config:
    """Pycln configs dataclass."""

    def __post_init__(self):
        if self.config is not None:
            file_path = self.config
            self.config = None
            ParseConfigFile(file_path, self)
        else:
            self._check_path()
            self._check_regex()
            self._parse_skip_imports()
            self._check_skip_imports()

    paths: list[Path]
    skip_imports: set[str]
    config: Optional[Path] = None
    include: Pattern[str] = regexu.INCLUDE_REGEX
    exclude: Pattern[str] = regexu.EXCLUDE_REGEX
    extend_exclude: Pattern[str] = regexu.EMPTY_REGEX
    all_: bool = False
    check: bool = False
    diff: bool = False
    verbose: bool = False
    quiet: bool = False
    silence: bool = False
    expand_stars: bool = False
    no_gitignore: bool = False
    disable_all_dunder_policy: bool = False

    def _parse_skip_imports(self) -> None:
        #: Converts "x,y,z" syntax into {"x", "y", "z"} set.
        #:
        #: Given {"x,y,z", "m", "n"}, `self.skip_imports`
        #: turns into {"x", "y", "z", "m", "n"}.
        pass

    def _check_path(self) -> None:
        # Validate `self.paths`.
        pass

    def _check_skip_imports(self) -> None:
        #: Validate `self.skip_imports`.
        #:
        #: NOTE: This method should be invocated
        #: just after `_parse_skip_imports`.
        pass

    def _check_regex(self) -> None:
        # Validate `self.include/exclude/extend_exclude`.
        pass


class ParseConfigFile:
    """Conifg file parser.

    :param file_path: config file path.
    :param config: Config instance as base.
    """

    def __init__(self, file_path: Path, config: Config):
        self._path = file_path
        self._config = config
        self._section = CONFIG_SECTIONS.get(self._path.suffix, None)
        self.parse()
        self._config.__post_init__()

    @staticmethod
    def _cast_paths(paths: list[str]) -> list[Path]:
        """`paths` List[str] ~> List[Path]."""
        pass

    def parse(self) -> None:
        """Get conifg from a `cfg`/`toml`/`json`/`yaml`/`yml` file."""
        pass

    def _parse_cfg(self) -> None:
        # Parse `.cfg` file.

        def cast_bool(v: str) -> Union[str, bool]:
            pass

        pass

    def _parse_toml(self) -> None:
        # Parse `.toml` file.
        pass

    def _parse_json(self) -> None:
        # Parse `.json` file.
        pass

    def _parse_yaml(self) -> None:
        # Parse `.yaml` file.
        pass

    def _parse_yml(self) -> None:
        # Support `.yml` file.
        pass

    def _config_loader(self, config_dict: dict) -> None:
        # k, v: config loader.
        pass
