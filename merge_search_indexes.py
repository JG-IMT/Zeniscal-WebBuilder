"""
Adds the search entries of the other Openflexo websites to the search index of a built website,
so that its search box also finds their pages.

The other websites are declared in website_settings.yml:
    extra:
      global_search:
        - name: Connie
          site_url: https://openflexo.org/connie/docs/

Usage (after "zensical build"):
    python merge_search_indexes.py --settings <website_settings.yml> --build-folder <folder>
"""
import argparse
from pathlib import Path

from webbuilder.search_index import SEARCH_INDEX_FILE_NAME, SearchIndex
from webbuilder.website_input import OUTPUT_FOLDER_NAME
from webbuilder.website_settings import WebsiteSettings


def _parse_arguments() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Adds the search entries of the other Openflexo websites to a built website."
    )
    parser.add_argument("--settings", type=Path, required=True, help="website_settings.yml of the project")
    parser.add_argument("--build-folder", type=Path, required=True, help="folder holding the built output/")
    return parser.parse_args()


if __name__ == "__main__":
    arguments: argparse.Namespace = _parse_arguments()
    settings: WebsiteSettings = WebsiteSettings(arguments.settings)
    search_index: SearchIndex = SearchIndex(
        arguments.build_folder / OUTPUT_FOLDER_NAME / SEARCH_INDEX_FILE_NAME, settings.site_url
    )
    added_entries_count: int = search_index.add_other_websites(settings.other_websites)
    search_index.save()
    print(f"Added {added_entries_count} search entries from {len(settings.other_websites)} other website(s)")
