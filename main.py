"""
Entry point of the website builder.

Usage:
    python main.py --build-websites
        Builds every website of the websites folder (next to the folder of the tool).
    python main.py --build-websites pamela connie
        Builds only the websites named.

A website is a sub-folder of the websites folder holding a website_settings.yml. Each version it declares is
cloned from git at its git_ref and built with Zensical. The website is assembled in websites/build/<name>:
the latest version at its root, each earlier version in a folder named after it.
"""

import argparse
from pathlib import Path

from webbuilder.building.merge_search_index import MergeSearchIndex
from webbuilder.building.website_build import WebsiteBuild
from webbuilder.repository.git_repository import GitRepository
from webbuilder.scanning.scan_website import ScanWebsite
from webbuilder.settings.website_settings import WebsiteSettings

WEBSITES_FOLDER: Path = Path(__file__).resolve().parent.joinpath("examples", "demo", "components", "websites")
SETTINGS_FILE_NAME: str = "website_settings.yml"
BUILD_FOLDER_NAME: str = "build"  # the websites as on the server, in the websites folder
PREPARATION_FOLDER_NAME: str = "preparation"  # the preparation of one website, next to its website_settings.yml
INDEX_FILE_NAME: str = "search.json"  # written by Zensical in each website, read by the search of its pages


# -- Build ----------------------------------------------------------------------------------------------

def _build_website(website_name: str, website_settings: WebsiteSettings) -> None:
    print(f"== Website {website_name}")
    git_repository: GitRepository = GitRepository(website_settings.get_repository_url())
    preparation_folder: Path = website_settings.get_folder().joinpath(PREPARATION_FOLDER_NAME)
    website_folder: Path = WEBSITES_FOLDER.joinpath(BUILD_FOLDER_NAME, website_settings.get_site_path())  # as on the server
    WebsiteBuild(website_settings, git_repository, preparation_folder, website_folder).build()


# -- Command line ---------------------------------------------------------------------------------------

def _parse_arguments() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Builds the websites, with all their versions, from the Markdown of their repositories, using Zensical."
    )
    # python main.py --build-websites pamela connie
    parser.add_argument(
        "--build-websites", nargs="*", required=True, metavar="NAME", help="names of the websites to build; none means all"
    )
    return parser.parse_args()


if __name__ == "__main__":
    arguments: argparse.Namespace = _parse_arguments()
    scan_website: ScanWebsite = ScanWebsite(WEBSITES_FOLDER, SETTINGS_FILE_NAME)
    website_settings_by_name: dict[str, WebsiteSettings] = {
        website_name: WebsiteSettings(settings_file) for website_name, settings_file in scan_website.get_settings_files([]).items()
    }
    for website_name in scan_website.get_settings_files(arguments.build_websites):
        _build_website(website_name, website_settings_by_name[website_name])

    # The search covers every website, also the ones not rebuilt now.
    merge_search_index: MergeSearchIndex = MergeSearchIndex(
        WEBSITES_FOLDER.joinpath(BUILD_FOLDER_NAME), PREPARATION_FOLDER_NAME, INDEX_FILE_NAME
    )
    merge_search_index.merge(website_settings_by_name)
