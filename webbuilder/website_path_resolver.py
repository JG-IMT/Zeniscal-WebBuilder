import posixpath
import re
from pathlib import Path


class WebsitePathResolver:
    """Decides where a path starting with "/" must point once the Markdown pages are in the website.

    A path starting with "/" leads to the root of the domain, not to the root of the website. Each one:
      1. the target is in the website: the path becomes relative to the page
      2. the path already starts with the project path (/my_project/javadoc/...): unchanged
      3. otherwise the project path is put in front (/javadoc/... becomes /my_project/javadoc/...),
         and a warning names the page and the path
    """

    def __init__(self, input_folder: Path, project_path: str = ""):
        self.input_folder: Path = input_folder
        self.project_path: str = project_path

    # -- Public: entry point ------------------------------------------------------------

    def resolve(self, link_path_without_first_slash: str, page_file: Path) -> str:
        if self._target_is_in_website(link_path_without_first_slash):
            return self._relative_to_page(link_path_without_first_slash, page_file)
        if self._needs_no_project_path(link_path_without_first_slash):
            return "/" + link_path_without_first_slash
        return self._with_project_path(link_path_without_first_slash, page_file)

    # -- Private: the three cases -------------------------------------------------------

    def _target_is_in_website(self, link_path_without_first_slash: str) -> bool:
        link_path_without_fragment_or_query: str = re.split(r"[#?]", link_path_without_first_slash)[0]
        return (self.input_folder / link_path_without_fragment_or_query).exists()

    def _relative_to_page(self, link_path_without_first_slash: str, page_file: Path) -> str:
        page_folder: str = page_file.parent.relative_to(self.input_folder).as_posix()
        return posixpath.relpath(link_path_without_first_slash, start=page_folder)

    def _needs_no_project_path(self, link_path_without_first_slash: str) -> bool:
        return not self.project_path or link_path_without_first_slash.startswith(self.project_path + "/")

    def _with_project_path(self, link_path_without_first_slash: str, page_file: Path) -> str:
        link_path_with_project_path: str = f"/{self.project_path}/{link_path_without_first_slash}"
        page_path_in_website: str = page_file.relative_to(self.input_folder).as_posix()
        original_link_path: str = "/" + link_path_without_first_slash
        print(f"Warning: {page_path_in_website}: {original_link_path} treated as {link_path_with_project_path}")
        return link_path_with_project_path
