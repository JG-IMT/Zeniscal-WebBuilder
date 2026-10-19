from pathlib import Path
from urllib.parse import urlparse

import yaml

from webbuilder.settings.website_versions import WebsiteVersions


TOOL_FOLDER: Path = Path(__file__).parent.parent.parent
SHARED_FOLDER: Path = TOOL_FOLDER / "shared"
SHARED_SETTINGS_FILE: Path = SHARED_FOLDER / "site_settings.yml"
SHARED_STYLE_AND_ICON_FOLDER: Path = SHARED_FOLDER / "style_and_icon"
SHARED_HTML_TEMPLATES_FOLDER: Path = SHARED_FOLDER / "html_templates"

SOURCES_KEY: str = "documentation_sources"
REPOSITORY_URL_KEY: str = "repository_url"
VERSIONS_KEY: str = "versions"
NAVIGATION_KEY: str = "nav"


class WebsiteSettings:
    """The settings shared by every website, completed by the settings of one project."""

    def __init__(self, project_settings_file: Path):
        self.project_settings_file: Path = project_settings_file
        self.values: dict = self._merge(read_yaml(SHARED_SETTINGS_FILE), read_yaml(project_settings_file))
        self._check_no_global_navigation()
        self.sources: list = self._extract_required_from_extra(SOURCES_KEY, "folders to copy")
        self.repository_url: str = self._extract_required_from_extra(REPOSITORY_URL_KEY, "repository to clone")
        declared_versions: list = self._extract_required_from_extra(VERSIONS_KEY, "versions to build")
        self.versions: WebsiteVersions = self._create_versions(declared_versions)

    # -- Public: settings ---------------------------------------------------------------

    @property
    def site_url(self) -> str:
        return self.values["site_url"]

    @property
    def project_path(self) -> str:
        """The project path on its domain, from "homepage" (https://openflexo.org/my_project/ gives "my_project")."""
        homepage_url: str = self.values["extra"].get("homepage", "")
        return urlparse(homepage_url).path.strip("/")

    # -- Private: extraction ------------------------------------------------------------

    def _extract_required_from_extra(self, key: str, purpose: str):
        extra: dict = self.values.get("extra") or {}
        if key not in extra:
            raise SystemExit(f"{self.project_settings_file}: no '{key}' under 'extra:' ({purpose})")
        return extra.pop(key)

    def _check_no_global_navigation(self) -> None:
        if NAVIGATION_KEY in self.values:
            raise SystemExit(f"{self.project_settings_file}: '{NAVIGATION_KEY}' would apply to every version; "
                             "put it in 'navigation' of the version it belongs to")

    # -- Private: versions --------------------------------------------------------------

    def _create_versions(self, declared_versions: list) -> WebsiteVersions:
        try:
            return WebsiteVersions(declared_versions, self.site_url)
        except ValueError as error:
            raise SystemExit(f"{self.project_settings_file}: {error}")

    # -- Private: merge -----------------------------------------------------------------

    @staticmethod
    def _merge(shared: dict, project: dict) -> dict:
        """The project wins; nested sections are merged key by key, lists are replaced."""
        merged: dict = dict(shared)
        for key, project_value in project.items():
            shared_value = shared.get(key)
            if isinstance(shared_value, dict) and isinstance(project_value, dict):
                merged[key] = WebsiteSettings._merge(shared_value, project_value)
            else:
                merged[key] = project_value
        return merged


# -- Public: YAML files -----------------------------------------------------------------

def read_yaml(file: Path) -> dict:
    return yaml.safe_load(file.read_text(encoding="utf-8"))


def write_yaml(file: Path, content: dict) -> None:
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(yaml.safe_dump(content, sort_keys=False, allow_unicode=True), encoding="utf-8")
