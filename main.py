"""
Entry point of the website builder.

Usage:
    python main.py build --settings <website_settings.yml>
        Clones each version declared in website_settings.yml at its git_ref, builds it with Zensical and
        assembles the website in <build folder>/website: the latest version at its root, each earlier
        version in a folder named after it. The "build" folder is created next to website_settings.yml.
"""

import argparse
from pathlib import Path

from webbuilder.building.website_build import WebsiteBuild
from webbuilder.repository.git_repository import GitRepository
from webbuilder.settings.website_settings import WebsiteSettings

BUILD_FOLDER_NAME: str = "build"


# -- Commands -------------------------------------------------------------------------------------------

def _build(arguments: argparse.Namespace) -> None:
    settings: WebsiteSettings = WebsiteSettings(arguments.settings)
    git_repository: GitRepository = GitRepository(settings.repository_url)
    WebsiteBuild(settings, git_repository, arguments.settings.parent / BUILD_FOLDER_NAME).build()


# -- Command line ---------------------------------------------------------------------------------------

def _existing_file(argument: str) -> Path:
    file: Path = Path(argument)
    if not file.is_file():
        raise argparse.ArgumentTypeError(f"{file} is not an existing file (expected a website_settings.yml)")
    return file


def _parse_arguments() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Website builder, based on Zensical.")
    commands = parser.add_subparsers(dest="command", required=True)

    # python main.py build --settings website_settings.yml
    build_parser = commands.add_parser("build", help="build every declared version and assemble the website")
    build_parser.add_argument("--settings", type=_existing_file, required=True,
                              help="website_settings.yml of the project")
    build_parser.set_defaults(run=_build)

    return parser.parse_args()


if __name__ == "__main__":
    arguments: argparse.Namespace = _parse_arguments()
    arguments.run(arguments)
