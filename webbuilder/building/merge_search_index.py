"""
Gives the search of each website the pages of all the websites. Zensical writes one search index per website,
which the search of the pages reads: the index of each website is replaced by the merge of the indexes of
all the websites. A page of another website is reached with a relative path, so the websites must be
side by side in the build folder as they are on the server: one folder per website, named after its address.
The pages of a website alone are kept next to its merged index, to merge again after another website is built.
"""

import json
import posixpath
from pathlib import Path

from webbuilder.settings.website_settings import WebsiteSettings


class MergeSearchIndex:
    """Replaces the search index of each built website by the merge of the indexes of all the built websites."""

    # -- Public: initialization ----------------------------------------------------------------------

    def __init__(self, build_folder: Path, index_file_name: str, own_index_file_name: str) -> None:
        self._build_folder: Path = build_folder  # holds the websites, one folder per address
        self._index_file_name: str = index_file_name  # read by the search of the pages
        self._own_index_file_name: str = own_index_file_name  # the pages of the website alone


    # -- Public: entry point -------------------------------------------------------------------------

    def merge(self, website_settings_by_name: dict[str, WebsiteSettings]) -> None:
        """Writes in each built website the merged index. A website that is not built yet is skipped."""
        built_settings_by_name: dict[str, WebsiteSettings] = self._keep_built_websites(website_settings_by_name)
        own_index_by_name: dict[str, dict] = {
            website_name: self._read_own_index(website_settings) for website_name, website_settings in built_settings_by_name.items()
        }
        for website_name in built_settings_by_name:
            merged_index: dict = self._merge_indexes(website_name, built_settings_by_name, own_index_by_name)
            self._find_index_file(built_settings_by_name[website_name]).write_text(json.dumps(merged_index), encoding="utf-8")
            print(f"Search: {website_name} searches {len(merged_index['items'])} pages of {len(own_index_by_name)} websites")


    # -- Private: reading ----------------------------------------------------------------------------

    def _find_index_file(self, website_settings: WebsiteSettings) -> Path:
        return self._build_folder.joinpath(website_settings.get_site_path(), self._index_file_name)


    def _keep_built_websites(self, website_settings_by_name: dict[str, WebsiteSettings]) -> dict[str, WebsiteSettings]:
        """The websites whose index exists in the build folder."""
        built_settings_by_name: dict[str, WebsiteSettings] = {}
        for website_name, website_settings in website_settings_by_name.items():
            if self._find_index_file(website_settings).is_file():
                built_settings_by_name[website_name] = website_settings
            else:
                print(f"Search: {website_name} is not built, skipped")
        return built_settings_by_name


    def _read_own_index(self, website_settings: WebsiteSettings) -> dict:
        """
        The index with the pages of the website alone. A website just built has none yet: its index is the one
        Zensical wrote, which is kept before being replaced by the merged one.
        """
        index_file: Path = self._find_index_file(website_settings)
        own_index_file: Path = index_file.with_name(self._own_index_file_name)
        if not own_index_file.is_file():
            own_index_file.write_text(index_file.read_text(encoding="utf-8"), encoding="utf-8")
        return json.loads(own_index_file.read_text(encoding="utf-8"))


    # -- Private: merging ----------------------------------------------------------------------------

    def _merge_indexes(
        self, website_name: str, website_settings_by_name: dict[str, WebsiteSettings], own_index_by_name: dict[str, dict]
    ) -> dict:
        """The index of the website, completed by the items of every other website."""
        merged_items: list[dict] = list(own_index_by_name[website_name]["items"])
        for other_name, other_settings in website_settings_by_name.items():
            if other_name != website_name:
                merged_items += self._items_seen_from(
                    website_settings_by_name[website_name], other_settings, own_index_by_name[other_name]["items"]
                )
        return {"config": own_index_by_name[website_name]["config"], "items": merged_items}


    @staticmethod
    def _items_seen_from(from_settings: WebsiteSettings, to_settings: WebsiteSettings, to_items: list[dict]) -> list[dict]:
        """The items of a website for the search of another one: a relative path to the pages, the website in the title."""
        # "." stands for a website at the root of the server, whose path is empty
        path_to_site: str = posixpath.relpath(to_settings.get_site_path() or ".", start=from_settings.get_site_path() or ".")
        return [
            {**item, "location": f"{path_to_site}/{item['location']}", "title": f"{to_settings.get_site_name()} · {item['title']}"}
            for item in to_items
        ]
