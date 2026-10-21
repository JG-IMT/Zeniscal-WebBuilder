"""
One version of a website, as declared in its settings: its name, the git reference it is built from, whether
it is the latest and optionally its own menu. The declaration is checked when it is read.
"""

import re

VERSION_NAME_PATTERN: re.Pattern = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
VERSION_DECLARATION_KEYS: tuple[str, ...] = ("name", "git_ref", "is_latest", "navigation")


class WebsiteVersion:
    """A version of the website: name, git reference to build it from, latest or not, and optionally its own menu."""

    # -- Public: initialization ----------------------------------------------------------------------

    def __init__(self, declaration: dict) -> None:
        self._check_declaration_keys(declaration)
        self.name: str = self._required_text(declaration, "name")
        self.git_ref: str = self._required_text(declaration, "git_ref")
        self.is_latest: bool = self._optional_boolean(declaration, "is_latest")
        self.navigation: list | None = self._optional_list(declaration, "navigation")
        self._check_name()


    # -- Private: declaration ------------------------------------------------------------------------

    @staticmethod
    def _check_declaration_keys(declaration: dict) -> None:
        if not isinstance(declaration, dict):
            raise ValueError(f"a version must be 'key: value' lines ({', '.join(VERSION_DECLARATION_KEYS)}), "
                             f"not {declaration!r}")
        unknown_keys: list[str] = []
        for key in declaration:
            if key not in VERSION_DECLARATION_KEYS:
                unknown_keys.append(key)
        if unknown_keys:
            raise ValueError(f"version {declaration}: unknown key(s) {unknown_keys}, "
                             f"known keys: {', '.join(VERSION_DECLARATION_KEYS)}")


    def _check_name(self) -> None:
        """The name is also the folder of the version in the website."""
        if not VERSION_NAME_PATTERN.fullmatch(self.name):
            raise ValueError(f"version name '{self.name}' may only contain letters, digits, '.', '_' and '-'")


    @staticmethod
    def _required_text(declaration: dict, key: str) -> str:
        value = declaration.get(key)
        if not isinstance(value, str):
            raise ValueError(f"version {declaration}: '{key}' is required and must be text (quote it: \"1.6\")")
        return value


    @staticmethod
    def _optional_boolean(declaration: dict, key: str) -> bool:
        value = declaration.get(key, False)
        if not isinstance(value, bool):
            raise ValueError(f"version {declaration}: '{key}' must be true or false")
        return value


    @staticmethod
    def _optional_list(declaration: dict, key: str) -> list | None:
        value = declaration.get(key)
        if value is not None and not isinstance(value, list):
            raise ValueError(f"version {declaration}: '{key}' must be a list")
        return value
