# Changelog

Changes since the tool was copied from the Pamela repository (`zensical_website_builder/`), made on
2026-10-15. The starting point was a single script, `prepare_website_build.py`, with the shared
files at the root of the folder.

## Tool (Zensical-WebBuilder, branch `dev`)

### Changed

- **Folders**: the shared files moved into `shared/` (`site_settings.yml`, `html_templates/`,
  `style_and_icon/`). `examples/website_settings.yml` is a template for a new repository.
- **Code in classes** (`webbuilder/`), one role each: `WebsiteSettings` (shared settings completed
  by the project's), `WebsiteInput` (input folder and Zensical config), `MarkdownLinks` (links of
  the pages), `SearchIndex` (`search.json`). Same output as the script it replaces.
- **Code style**: sections `# -- Public / Private --` (public first), explicit steps instead of
  dense one-liners, private helpers as static methods, lines of 120 characters at most.
- **One entry point**, `main.py`, with two commands: `prepare` (replaces `prepare_website_build.py`)
  and `search`.
- **Build folder**: always `build/` next to `website_settings.yml`. The `--build-folder` option is
  removed.
- **`--settings`** must be an existing file (a folder is refused) and says so clearly.
- **README** rewritten (install, use, features), Python 3.11 to 3.13 stated in the README and in
  `requirements.txt`, no mention of a particular project in the tool.

### Added

- **Links starting with "/"** are fixed in the copies of the pages (never in the sources):
  relative when the target is in the website, unchanged when they already start with the project
  path, otherwise the project path is put in front. The project path comes from `homepage`.
- **Global search** (`main.py search`): the pages of other websites, declared under `global_search`,
  are added to `search.json`. Same domain required.
- **Banner on earlier versions** (`prepare --latest-version 1.6.1`): the menu lists the latest
  version first, the built version is marked as current, and every page links to the latest version.

### Removed

- `prepare_website_build.py`, `merge_search_indexes.py` (replaced by `main.py`), the `--build-folder`
  option.

### Fixed

- `.gitignore`: `.__pycache__/` became `__pycache__/`.

## Pamela (branch `julien-clean`, from `1.6.1`)

Nothing existing was changed: no Markdown, no image, no folder moved. Three additions:

- `zensical_website_builder/`: copy of the tool (19 files), kept in sync by hand.
- `pamela_website/website_settings.yml`: name, menu, Markdown folders (`resources/images`, `img`,
  `examples`), previous versions, links of the top bar.
- `build.gradle`: block "Documentation website (Zensical)" with four tasks, run with
  `./gradlew buildDocumentationSite`; the site is written to `pamela_website/build/output`.

## Checked

- Pamela `1.6.1`: 29 pages, 20 links fixed, 0 broken link out of 1,377.
- Earlier versions rebuilt from their branches: `1.6` (29 pages) and `1.5.0.1` (7 pages), with
  banner and menu; the menus, banners and 2,896 internal links of the three assembled versions
  checked, 0 broken.
- Global search between two sites on the same domain: 78 entries added, results lead to the right page.
