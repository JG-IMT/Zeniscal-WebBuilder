"""
Merges the search index Zensical wrote for each website into one index for all the websites. It reads the
latest version of each website as it is in the build folder, so a website not rebuilt keeps its entries.
"""

import html
import json
import re
from pathlib import Path

from webbuilder.settings.website_settings import WebsiteSettings


class MergeSearchIndex:
    """Merges the search indexes of the built websites into one global search index."""

    # -- Public: initialization ----------------------------------------------------------------------

    def __init__(self, build_folder: Path, website_index_file_name: str, global_index_file_name: str) -> None:
        self._build_folder: Path = build_folder  # holds one folder per website
        self._website_index_file_name: str = website_index_file_name
        self._global_index_file: Path = build_folder.joinpath(global_index_file_name)


    # -- Public: entry point -------------------------------------------------------------------------

    def merge(self, settings_file_by_website_name: dict[str, Path]) -> None:
        """
        Writes the global index: the address of each website, and the entries of all of them.
        A website that is not built yet is skipped.
        """
        website_urls: dict[str, str] = {}
        entries: list[dict] = []
        for website_name, settings_file in settings_file_by_website_name.items():
            website_index_file: Path = self._build_folder.joinpath(website_name, self._website_index_file_name)
            if not website_index_file.is_file():
                print(f"Search: {website_name} is not built, skipped")
                continue
            website_urls[website_name] = self._read_website_url(settings_file)
            entries += self._read_entries(website_name, website_index_file)

        self._global_index_file.write_text(json.dumps({"websites": website_urls, "entries": entries}), encoding="utf-8")
        print(f"Search: {len(entries)} entries of {len(website_urls)} websites in {self._global_index_file}")


    # -- Private: reading ----------------------------------------------------------------------------

    @staticmethod
    def _read_website_url(settings_file: Path) -> str:
        """The address of the latest version of the website."""
        version_catalog = WebsiteSettings(settings_file).get_version_catalog()
        return version_catalog.site_url_of(version_catalog.get_latest_version())


    @staticmethod
    def _read_entries(website_name: str, website_index_file: Path) -> list[dict]:
        """The entries of a website index, with their text freed from HTML."""
        website_items: list[dict] = json.loads(website_index_file.read_text(encoding="utf-8"))["items"]
        return [
            {
                "website": website_name,
                "title": item["title"],
                "location": item["location"],
                "text": html.unescape(re.sub(r"<[^>]+>", " ", item["text"])),
            }
            for item in website_items
        ]
