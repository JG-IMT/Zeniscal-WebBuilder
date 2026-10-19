"""
Entry point of the website builder.

Usage:
    python main.py prepare --settings <website_settings.yml> [--version 1.2.3] [--clean]
        Prepares what Zensical needs: the input folder (the Markdown and images of the repository containing
        website_settings.yml, plus the files shared by every website) and the config file, for a version
        declared in website_settings.yml (default: the latest). Everything generated goes to the "build"
        folder next to website_settings.yml. Then build with:
        zensical build -f <build folder>/zensical_config.yml

    python main.py search --settings <website_settings.yml>
        After the build, adds the pages of the websites declared under extra.global_search
        (website_settings.yml) to the search index of the built website:
            extra:
              global_search:
                - name: Other project
                  site_url: https://openflexo.org/other_project/docs/
"""
import argparse
from pathlib import Path

from webbuilder.git_repository import GitRepository
from webbuilder.search_index import SEARCH_INDEX_FILE_NAME, SearchIndex
from webbuilder.website_input import OUTPUT_FOLDER_NAME, WebsiteInput
from webbuilder.website_settings import WebsiteSettings
from webbuilder.website_version import WebsiteVersion

BUILD_FOLDER_NAME: str = "build"


# -- Commands ---------------------------------------------------------------------------

def _prepare(arguments: argparse.Namespace) -> None:
    settings: WebsiteSettings = WebsiteSettings(arguments.settings)
    version: WebsiteVersion = settings.version_named(arguments.version) if arguments.version else settings.latest_version
    repository_folder: Path = GitRepository.find_root_containing(arguments.settings.parent)
    build_folder: Path = arguments.settings.parent / BUILD_FOLDER_NAME
    website_input: WebsiteInput = WebsiteInput(settings, repository_folder, build_folder, version)
    print(f"Zensical config: {website_input.prepare(arguments.clean)}")


def _search(arguments: argparse.Namespace) -> None:
    build_folder: Path = arguments.settings.parent / BUILD_FOLDER_NAME
    settings: WebsiteSettings = WebsiteSettings(arguments.settings)
    search_index: SearchIndex = SearchIndex(
        build_folder / OUTPUT_FOLDER_NAME / SEARCH_INDEX_FILE_NAME, settings.site_url
    )
    added_entries_count: int = search_index.add_other_websites(settings.other_websites)
    search_index.save()
    print(f"Added {added_entries_count} search entries from {len(settings.other_websites)} other website(s)")


# -- Command line -----------------------------------------------------------------------

def _existing_file(argument: str) -> Path:
    file: Path = Path(argument)
    if not file.is_file():
        raise argparse.ArgumentTypeError(f"{file} is not an existing file (expected a website_settings.yml)")
    return file


def _parse_arguments() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Website builder, based on Zensical.")
    commands = parser.add_subparsers(dest="command", required=True)

    prepare_parser = commands.add_parser("prepare", help="prepare the input folder and the config of Zensical")
    prepare_parser.add_argument("--version", help="version to prepare (default: the latest)")
    prepare_parser.add_argument("--clean", action="store_true", help="delete the input folder first")
    prepare_parser.set_defaults(run=_prepare)

    search_parser = commands.add_parser("search", help="add the pages of other websites to the search index")
    search_parser.set_defaults(run=_search)

    for command_parser in (prepare_parser, search_parser):
        command_parser.add_argument("--settings", type=_existing_file, required=True,
                                    help="website_settings.yml of the project")
    return parser.parse_args()


if __name__ == "__main__":
    arguments: argparse.Namespace = _parse_arguments()
    arguments.run(arguments)
