import subprocess
import sys
from pathlib import Path

from webbuilder.repository.git_repository import GitRepository
from webbuilder.preparation.website_input import OUTPUT_FOLDER_NAME, WebsiteInput
from webbuilder.settings.website_settings import WebsiteSettings
from webbuilder.settings.website_versions import WebsiteVersion

REPOSITORY_FOLDER_NAME: str = "repository"


class VersionBuild:
    """The build of one version: its clone, its input folder and its built pages."""

    def __init__(self, settings: WebsiteSettings, repository: GitRepository, version: WebsiteVersion,
                 build_folder: Path):
        self.settings: WebsiteSettings = settings
        self.repository: GitRepository = repository
        self.version: WebsiteVersion = version
        self.build_folder: Path = build_folder
        self.repository_folder: Path = build_folder / REPOSITORY_FOLDER_NAME
        self.output_folder: Path = build_folder / OUTPUT_FOLDER_NAME

    # -- Public: entry point ------------------------------------------------------------

    def build(self) -> Path:
        print(f"Building version {self.version.name} ({self.version.git_ref})")
        self.repository.clone_at(self.version.git_ref, self.repository_folder)
        website_input: WebsiteInput = WebsiteInput(self.settings, self.repository_folder, self.build_folder,
                                                   self.version)
        self._run_zensical(website_input.prepare(clean_first=True))
        return self.output_folder

    # -- Private: steps -----------------------------------------------------------------

    def _run_zensical(self, zensical_config_file: Path) -> None:
        """Zensical is the one installed for the Python running this tool."""
        result: subprocess.CompletedProcess = subprocess.run(
            [sys.executable, "-m", "zensical", "build", "--clean", "-f", str(zensical_config_file)]
        )
        if result.returncode != 0:
            raise SystemExit(f"Zensical failed on version {self.version.name}")
