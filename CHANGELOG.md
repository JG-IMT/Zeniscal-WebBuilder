# Changelog

Changes since the tool was copied from the Pamela repository (`zensical_website_builder/`), made on
2026-10-15. The starting point was a single script, `prepare_website_build.py`, with the shared
files at the root of the folder.

## Tool (Zensical-WebBuilder, branch `dev`)

### 2026-10-19: every version built from git

#### Added

- **Versions declared in `website_settings.yml`** (`extra.repository_url`, `extra.versions`): name,
  `git_ref` (branch or tag), `is_latest`, optional `navigation`. Classes `WebsiteVersion`, `WebsiteVersions` and
  `GitRepository` (shallow clone).
- **`main.py build`**: clones each version, prepares it, runs Zensical and assembles `build/output` (latest version at the root, the others
  in `<name>/`). Classes `VersionBuild` and `WebsiteBuild`. `--repository-url` replaces the declared
  repository (a fork, a local folder).
- **`main.py serve`**: serves `build/output` on a local port.
- **Checks that stop the build**: version name not text or with forbidden characters, duplicated
  names, not exactly one latest version, a top-level `nav`, a git reference that cannot be cloned,
  a source folder missing, no Markdown page.
- **Version menu**: same page in the chosen version when it exists, otherwise its home page, with
  links relative to the displayed version (the local website stays local).
- **Per version**: its own `site_url` (sitemap, canonical link), its own `navigation` when declared,
  the banner of an earlier version links to the latest one (`extra.latest_version_url`).

#### Changed

- **`documentation_sources` are relative to the repository root**, no longer to `website_settings.yml`.
- **`prepare`** prepares the latest version from the working folder, to write the documentation.
  `--version` and `--latest-version` are removed.

- **Paths starting with "/"**: `MarkdownLinks` replaced by `WebsitePathResolver` (decides where a path
  must point) and `MarkdownPathRewriter` (rewrites the paths of the page files). A path whose project
  path is guessed prints a warning naming the page. Line endings and BOM are kept, a page that is not
  UTF-8 is refused with its name. The Markdown page files are listed by `VersionSiteInput`.

- **Code by role** (`webbuilder/`): `settings/` (`WebsiteSettings`, `WebsiteVersion`, `WebsiteVersions`), `repository/`
  (`GitRepository`), `preparation/` (`VersionSiteInput`, `WebsitePathResolver`, `MarkdownPathRewriter`),
  `building/` (`VersionBuild`, `WebsiteBuild`).

- **Settings checked when they are read**: a missing or non-text `site_url`, an empty file, invalid
  YAML, `extra` or `versions` of the wrong kind, a source without `source` and `destination`, a
  non-text `repository_url`, an unknown key, a non-boolean `is_latest` or a non-list `navigation` in a
  version now stop with one line naming the file (some were raw errors, others were accepted).
- **One owner for the layout of the versions**: `WebsiteVersions.folder_of` ("." for the latest, its
  name for the others) is used by `site_url_of`, `VersionSiteInput` and `WebsiteBuild`, which each wrote
  the rule themselves.
- **`repository_url` is optional in the settings**: `prepare` never needed it and `build --repository-url`
  replaces it. `build` stops with one line if neither gives a repository
  (`WebsiteSettings.repository_url_to_clone`). Less public surface: `WebsiteSettings.site_url` and
  `project_settings_file`, `WebsiteVersions.site_url` and `versions_in_declared_order` are internal,
  `WebsiteVersions.__len__` and the `repository_url` type check are removed.
- **Names and places**: `WebsiteSettings.values` is `zensical_values`, `project_path` is
  `project_url_path` (also in `WebsitePathResolver`), `_extract_required_from_extra` is
  `_pop_required_from_extra`. The folders of the tool (`TOOL_FOLDER`, `SHARED_*`) moved to
  `webbuilder/shared_files.py`, and reading or writing YAML is private to the class that does it.

#### Removed

- `previous_versions` (links written by hand, replaced by `versions`) and the top-level `nav`.
- **Search across components**: `SearchIndex`, the `search` command and `extra.global_search`, until it
  is ready for production. Each version keeps the search of its own pages.

### 2026-10-15: the tool outside Pamela

#### Changed

- **Folders**: the shared files moved into `shared/` (`site_settings.yml`, `html_templates/`,
  `style_and_icon/`). `examples/website_settings.yml` is a template for a new repository.
- **Code in classes** (`webbuilder/`), one role each: `WebsiteSettings` (shared settings completed
  by the project's), `VersionSiteInput` (input folder and Zensical config), `MarkdownLinks` (links of
  the pages), `SearchIndex` (`search.json`). Same output as the script it replaces.
- **Code style**: sections `# -- Public / Private --` (public first), explicit steps instead of
  dense one-liners, private helpers as static methods, lines of 120 characters at most.
- **One entry point**, `main.py`, with two commands: `prepare` (replaces `prepare_website_build.py`)
  and `search` (`build` and `serve` were added on 2026-10-19).
- **Build folder**: always `build/` next to `website_settings.yml`. The `--build-folder` option is
  removed.
- **`--settings`** must be an existing file (a folder is refused) and says so clearly.
- **README** rewritten (install, use, features), Python 3.11 to 3.13 stated in the README and in
  `requirements.txt`, no mention of a particular project in the tool.

#### Added

- **Links starting with "/"** are fixed in the copies of the pages (never in the sources):
  relative when the target is in the website, unchanged when they already start with the project
  path, otherwise the project path is put in front. The project path comes from `homepage`.
- **Global search** (`main.py search`, removed on 2026-10-19): the pages of other websites, declared under `global_search`,
  are added to `search.json`. Same domain required.
- **Banner on earlier versions** (`--latest-version`, replaced on 2026-10-19 by `versions`): the menu lists the latest
  version first, the built version is marked as current, and every page links to the latest version.

#### Removed

- `prepare_website_build.py`, `merge_search_indexes.py` (replaced by `main.py`), the `--build-folder`
  option.

#### Fixed

- `.gitignore`: `.__pycache__/` became `__pycache__/`.

## Pamela (branch `julien-clean`, from `1.6.1`)

Not migrated yet to the 2026-10-19 version of the tool (`versions`, sources relative to the
repository root, `build`). State of 2026-10-15: nothing existing was changed: no Markdown, no image,
no folder moved. Three additions:

- `zensical_website_builder/`: copy of the tool (19 files), kept in sync by hand.
- `pamela_website/website_settings.yml`: name, menu, Markdown folders (`resources/images`, `img`,
  `examples`), previous versions, links of the top bar.
- `build.gradle`: block "Documentation website (Zensical)" with four tasks, run with
  `./gradlew buildDocumentationSite`; the site is written to `pamela_website/build/output`.

## Checked

2026-10-19, on clones of Pamela (`1.6.1`, `1.6`, `1.5.0.1`) with Zensical 0.0.70, by hand:

- `build` of the three versions, twice in a row: Zensical "No issues found" each time, 29, 29 and 7
  pages, versions assembled at the root, in `1.6/` and in `1.5.0.1/`; clones deleted on Windows.
- A git reference that does not exist stops the build; `serve` answers 200 on the pages, the
  search index and the images, 404 on a missing page.
- Version menu opened in a browser on five pages: same page in the other version when it exists,
  home page of the version otherwise.
- Not checked: the rendering of the pages, results of another website's search, a production server.

2026-10-15:

- Pamela `1.6.1`: 29 pages, 20 links fixed, 0 broken link out of 1,377.
- Earlier versions rebuilt from their branches: `1.6` (29 pages) and `1.5.0.1` (7 pages), with
  banner and menu; the menus, banners and 2,896 internal links of the three assembled versions
  checked, 0 broken.
- Global search between two sites on the same domain: 78 entries added, results lead to the right page.
