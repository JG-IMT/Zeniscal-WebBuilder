import posixpath
import re
from pathlib import Path

# "](/images/a.png)", src="/images/a.png" and href="/files/a.zip", but not "//host/..."
ROOT_LINK_PATTERN: re.Pattern = re.compile(r'(\]\(|\b(?:src|href)=")/(?!/)([^)"\s]+)')
CODE_FENCE_PATTERN: re.Pattern = re.compile(r"^\s*(```|~~~)")


class MarkdownLinks:
    """The Markdown pages of the input folder, whose links starting with "/" are made relative.

    A link starting with "/" leads to the root of the domain, not to the root of the website, so it
    breaks once the website is published under a sub-path (e.g. openflexo.org/<project>/docs/).
    Only the copies in the input folder are changed, never the sources.
    """

    def __init__(self, input_folder: Path):
        self.input_folder: Path = input_folder

    def make_relative(self) -> int:
        converted_links_count: int = 0
        for page in self.input_folder.rglob("*.md"):
            page_folder: str = page.parent.relative_to(self.input_folder).as_posix()
            new_lines, count = self._convert_lines(page.read_text(encoding="utf-8").split("\n"), page_folder)
            if count:
                page.write_text("\n".join(new_lines), encoding="utf-8")
            converted_links_count += count
        return converted_links_count

    @staticmethod
    def _convert_lines(lines: list, page_folder: str) -> tuple:
        """Lines inside a code block are left as they are."""
        converted_links_count: int = 0
        inside_code_block: bool = False

        def to_relative_link(match: re.Match) -> str:
            nonlocal converted_links_count
            converted_links_count += 1
            return match.group(1) + posixpath.relpath(match.group(2), start=page_folder)

        new_lines: list = []
        for line in lines:
            if CODE_FENCE_PATTERN.match(line):
                inside_code_block = not inside_code_block
            new_lines.append(line if inside_code_block else ROOT_LINK_PATTERN.sub(to_relative_link, line))
        return new_lines, converted_links_count
