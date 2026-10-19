import re
from typing import Iterator

VERSION_NAME_PATTERN: re.Pattern = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


class WebsiteVersion:
    """A version of the documentation: the git reference it is built from, and optionally its own menu."""

    def __init__(self, declaration: dict):
        self.name: str = self._required_text(declaration, "name")
        self.git_ref: str = self._required_text(declaration, "git_ref")
        self.is_latest: bool = bool(declaration.get("is_latest", False))
        self.navigation: list | None = declaration.get("navigation")
        if not VERSION_NAME_PATTERN.fullmatch(self.name):
            raise ValueError(f"version name '{self.name}' may only contain letters, digits, '.', '_' and '-'")

    # -- Private: declaration -----------------------------------------------------------

    @staticmethod
    def _required_text(declaration: dict, key: str) -> str:
        value = declaration.get(key)
        if not isinstance(value, str):
            raise ValueError(f"version {declaration}: '{key}' is required and must be text (quote it: \"1.6\")")
        return value


class WebsiteVersions:
    """The versions of a website: the latest is served at the website URL, the others in a folder named after them."""

    def __init__(self, declared_versions: list, site_url: str):
        self.site_url: str = site_url.rstrip("/") + "/"
        self.versions_in_declared_order: list = [WebsiteVersion(declaration) for declaration in declared_versions or []]
        self._check_names_are_unique()
        self._check_exactly_one_is_latest()

    # -- Public: the versions -----------------------------------------------------------

    def __iter__(self) -> Iterator[WebsiteVersion]:
        return iter(self.versions_in_declared_order)

    def __len__(self) -> int:
        return len(self.versions_in_declared_order)

    @property
    def latest(self) -> WebsiteVersion:
        return next(version for version in self if version.is_latest)

    @property
    def earlier(self) -> list:
        return [version for version in self if not version.is_latest]

    def site_url_of(self, version: WebsiteVersion) -> str:
        if version.is_latest:
            return self.site_url
        return f"{self.site_url}{version.name}/"

    # -- Private: checks ----------------------------------------------------------------

    def _check_names_are_unique(self) -> None:
        names: list = [version.name for version in self]
        if len(set(names)) != len(names):
            raise ValueError("version names must be unique")

    def _check_exactly_one_is_latest(self) -> None:
        latest_versions_count: int = sum(version.is_latest for version in self)
        if latest_versions_count != 1:
            raise ValueError(f"exactly one version must have 'is_latest: true' (found {latest_versions_count})")
