"""
Gives the search of each website the pages of all the websites. Zensical writes one search index per website,
which the search of the pages reads: the index of each website is replaced by the merge of the indexes of
all the websites. A page of another website is reached with a relative path, so the websites must be
side by side in the build folder as they are on the server: one folder per website, named after its address.
"""

import json
import posixpath
from pathlib import Path

from webbuilder.building.website_build import VERSION_BUILDS_FOLDER_NAME
from webbuilder.preparation.zensical_input import VERSION_SITE_FOLDER_NAME
from webbuilder.settings.website_settings import WebsiteSettings


class MergeSearchIndex:
    """Replaces the search index of each built website by the merge of the indexes of all the built websites."""

    # -- Public: initialization ----------------------------------------------------------------------

    def __init__(self, build_folder: Path, work_folder_name: str, index_file_name: str) -> None:
        self._build_folder: Path = build_folder  # holds the websites, one folder per address
        self._work_folder_name: str = work_folder_name  # in the folder of the settings of each website
        self._index_file_name: str = index_file_name


    # -- Public: entry point -------------------------------------------------------------------------

    def merge(self, settings_file_by_website_name: dict[str, Path]) -> None:
        """Writes in each built website the merged index. A website that is not built yet is skipped."""
        website_settings_by_name: dict[str, WebsiteSettings] = self._read_built_websites(settings_file_by_website_name)
        index_by_name: dict[str, dict] = {
            website_name: self._read_zensical_index(settings_file_by_website_name[website_name], website_settings)
            for website_name, website_settings in website_settings_by_name.items()
        }
        for website_name in website_settings_by_name:
            merged_index: dict = self._merge_indexes(website_name, website_settings_by_name, index_by_name)
            self._write_index(website_settings_by_name[website_name], merged_index)
            print(f"Search: {website_name} searches {len(merged_index['items'])} pages of {len(index_by_name)} websites")


    # -- Private: reading ----------------------------------------------------------------------------

    def _read_built_websites(self, settings_file_by_website_name: dict[str, Path]) -> dict[str, WebsiteSettings]:
        """The settings of the websites whose index exists, by website name."""
        website_settings_by_name: dict[str, WebsiteSettings] = {}
        for website_name, settings_file in settings_file_by_website_name.items():
            website_settings: WebsiteSettings = WebsiteSettings(settings_file)
            if self._find_zensical_index(settings_file, website_settings).is_file():
                website_settings_by_name[website_name] = website_settings
            else:
                print(f"Search: {website_name} is not built, skipped")
        return website_settings_by_name


    def _find_zensical_index(self, settings_file: Path, website_settings: WebsiteSettings) -> Path:
        """The index Zensical wrote for the latest version, kept in the work folder: the build folder holds the merged one."""
        latest_version_name: str = website_settings.get_version_catalog().get_latest_version().get_name()
        return settings_file.parent.joinpath(
            self._work_folder_name, VERSION_BUILDS_FOLDER_NAME, latest_version_name, VERSION_SITE_FOLDER_NAME, self._index_file_name
        )


    def _read_zensical_index(self, settings_file: Path, website_settings: WebsiteSettings) -> dict:
        return json.loads(self._find_zensical_index(settings_file, website_settings).read_text(encoding="utf-8"))


    # -- Private: merging ----------------------------------------------------------------------------

    def _merge_indexes(
        self, website_name: str, website_settings_by_name: dict[str, WebsiteSettings], index_by_name: dict[str, dict]
    ) -> dict:
        """The index of the website, completed by the items of every other website."""
        merged_items: list[dict] = list(index_by_name[website_name]["items"])
        for other_name, other_settings in website_settings_by_name.items():
            if other_name != website_name:
                merged_items += self._items_seen_from(
                    website_settings_by_name[website_name], other_settings, index_by_name[other_name]["items"]
                )
        return {"config": index_by_name[website_name]["config"], "items": merged_items}


    @staticmethod
    def _items_seen_from(from_settings: WebsiteSettings, to_settings: WebsiteSettings, to_items: list[dict]) -> list[dict]:
        """The items of a website for the search of another one: a relative path to the pages, the website in the title."""
        path_to_site: str = posixpath.relpath(to_settings.get_site_path(), start=from_settings.get_site_path())
        return [
            {**item, "location": f"{path_to_site}/{item['location']}", "title": f"{to_settings.get_site_name()} · {item['title']}"}
            for item in to_items
        ]


    # -- Private: writing ----------------------------------------------------------------------------

    def _write_index(self, website_settings: WebsiteSettings, merged_index: dict) -> None:
        """Replaces the index of the website in the build folder, where its pages read it."""
        index_file: Path = self._build_folder.joinpath(website_settings.get_site_path(), self._index_file_name)
        index_file.write_text(json.dumps(merged_index), encoding="utf-8")
