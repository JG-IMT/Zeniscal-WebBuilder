import json
import os
import shutil
from pathlib import Path

from webbuilder.website_settings import (
    SHARED_HTML_TEMPLATES_FOLDER, SHARED_STYLE_AND_ICON_FOLDER, WebsiteSettings, write_yaml,
)

INPUT_FOLDER_NAME: str = "input"
OUTPUT_FOLDER_NAME: str = "output"
ZENSICAL_CONFIG_FILE_NAME: str = "zensical_config.yml"
VERSIONS_FILE_NAME: str = "versions.json"


class WebsiteInput:
    """What Zensical builds a website from: the input folder and its config file."""

    def __init__(self, settings: WebsiteSettings, build_folder: Path, displayed_version: str):
        self.settings: WebsiteSettings = settings
        self.displayed_version: str = displayed_version
        self.input_folder: Path = build_folder / INPUT_FOLDER_NAME
        self.zensical_config_file: Path = build_folder / ZENSICAL_CONFIG_FILE_NAME

    def prepare(self, clean_first: bool) -> Path:
        if clean_first:
            self._delete_input_folder()

        _copy_folder(SHARED_STYLE_AND_ICON_FOLDER, self.input_folder)
        self._copy_declared_sources()
        self._write_versions_file()
        self._write_zensical_config()

        print(f"Prepared {self._count_markdown_pages()} Markdown pages in {self.input_folder}")
        return self.zensical_config_file

    def _copy_declared_sources(self) -> None:
        for source_entry in self.settings.sources:
            source_folder: Path = self.settings.project_settings_file.parent / source_entry["source"]
            _copy_folder(source_folder, self.input_folder / source_entry["destination"])

    def _write_versions_file(self) -> None:
        """Read by the version menu of every page: the current version first, then the earlier ones."""
        current_version: dict = {"name": self.displayed_version, "link": self.settings.site_url, "current": True}
        versions: list = [current_version] + self.settings.previous_versions
        (self.input_folder / VERSIONS_FILE_NAME).write_text(json.dumps(versions, indent=2), encoding="utf-8")

    def _write_zensical_config(self) -> None:
        """Paths are relative to the generated config file, which is where Zensical reads them from."""
        values: dict = self.settings.values
        templates_path: str = os.path.relpath(SHARED_HTML_TEMPLATES_FOLDER, self.zensical_config_file.parent)
        values["docs_dir"] = INPUT_FOLDER_NAME
        values["site_dir"] = OUTPUT_FOLDER_NAME
        values["theme"]["custom_dir"] = Path(templates_path).as_posix()
        values["extra"]["displayed_version"] = self.displayed_version
        write_yaml(self.zensical_config_file, values)

    def _delete_input_folder(self) -> None:
        """Not the default: under a running "zensical serve" it loses the stylesheet."""
        if self.input_folder.exists():
            shutil.rmtree(self.input_folder)

    def _count_markdown_pages(self) -> int:
        return sum(1 for _ in self.input_folder.rglob("*.md"))


def _copy_folder(source_folder: Path, destination_folder: Path) -> None:
    shutil.copytree(source_folder, destination_folder, dirs_exist_ok=True)
