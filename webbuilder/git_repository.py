import subprocess
from pathlib import Path


class GitRepository:
    """A git repository, cloned to build one of its versions."""

    def __init__(self, repository_url: str):
        self.repository_url: str = repository_url

    # -- Public: clone ------------------------------------------------------------------

    def clone_at(self, git_ref: str, destination_folder: Path) -> None:
        command: list = ["git", "-c", "core.longpaths=true", "clone", "--quiet", "--depth", "1",
                         "--branch", git_ref, self.repository_url, str(destination_folder)]
        try:
            result: subprocess.CompletedProcess = subprocess.run(command, capture_output=True, text=True)
        except FileNotFoundError:
            raise SystemExit("git is not installed or not in the PATH")
        if result.returncode != 0:
            raise SystemExit(f"Cannot clone {self.repository_url} at '{git_ref}': {result.stderr.strip()}")
