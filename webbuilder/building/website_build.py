import os
import shutil
import stat
from pathlib import Path

from webbuilder.building.version_build import VersionBuild
from webbuilder.preparation.website_input import OUTPUT_FOLDER_NAME
from webbuilder.repository.git_repository import GitRepository
from webbuilder.settings.website_settings import WebsiteSettings

VERSIONS_FOLDER_NAME: str = "versions"


class WebsiteBuild:
    """The build of every version of the website, assembled in a single output folder."""

    def __init__(self, settings: WebsiteSettings, repository: GitRepository, build_folder: Path):
        self.settings: WebsiteSettings = settings
        self.repository: GitRepository = repository
        self.versions_folder: Path = build_folder / VERSIONS_FOLDER_NAME
        self.output_folder: Path = build_folder / OUTPUT_FOLDER_NAME

    # -- Public: entry point ------------------------------------------------------------

    def build(self) -> Path:
        self._delete_folder(self.versions_folder)
        self._delete_folder(self.output_folder)
        for version in self.settings.versions:
            version_build: VersionBuild = VersionBuild(self.settings, self.repository, version,
                                                       self.versions_folder / version.name)
            version_output_folder: Path = self.output_folder / self.settings.versions.folder_of(version)
            shutil.copytree(version_build.build(), version_output_folder, dirs_exist_ok=True)
        print(f"Website of {len(self.settings.versions)} version(s) in {self.output_folder}")
        return self.output_folder

    # -- Private: folders ---------------------------------------------------------------

    @staticmethod
    def _delete_folder(folder: Path) -> None:
        if folder.exists():
            shutil.rmtree(folder, onerror=WebsiteBuild._retry_after_making_writable)

    @staticmethod
    def _retry_after_making_writable(delete_function, path: str, _error) -> None:
        """On Windows, the files git writes in a clone are read-only and cannot be deleted as they are."""
        os.chmod(path, stat.S_IWRITE)
        delete_function(path)
