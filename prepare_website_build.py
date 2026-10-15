"""
Prepares what Zensical needs to build a website:
  - the input folder: the project's Markdown and images, plus the files shared by every website
  - the config file: the shared settings completed by the project's own settings

Usage:
    python prepare_website_build.py --settings <website_settings.yml> --build-folder <folder>
                                    [--version 1.2.3] [--clean]
Then build with:  zensical build -f <folder>/zensical_config.yml
"""
import argparse
from pathlib import Path

from webbuilder.website_input import WebsiteInput
from webbuilder.website_settings import WebsiteSettings

DEFAULT_VERSION: str = "dev"


def _parse_arguments() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Prepares the input folder and the config Zensical builds a website from."
    )
    parser.add_argument("--settings", type=Path, required=True, help="website_settings.yml of the project")
    parser.add_argument("--build-folder", type=Path, required=True, help="folder receiving everything generated")
    parser.add_argument("--version", default=DEFAULT_VERSION, help="version shown in the website")
    parser.add_argument("--clean", action="store_true", help="delete the input folder first")
    return parser.parse_args()


if __name__ == "__main__":
    arguments: argparse.Namespace = _parse_arguments()
    website_input: WebsiteInput = WebsiteInput(
        WebsiteSettings(arguments.settings), arguments.build_folder, arguments.version
    )
    print(f"Zensical config: {website_input.prepare(arguments.clean)}")
