# Website builder

Builds the documentation websites of the OpenFlexo projects (Pamela, Connie, ...), with all their versions,
from the Markdown of their git repositories, using [Zensical](https://zensical.org). The tool, the theme and
the OpenFlexo footer are the same for every project, a project only brings a `website_settings.yml`.

## What a project needs

- a git repository holding its documentation as Markdown files.
- a `website_settings.yml` saying where the documentation is, which versions to build and how the website
  looks. Start from `examples/website_settings.yml`, for now the name of the folder is the name of the website.

## Install (once)

Needs Python 3.11 or later and git.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

On Linux and macOS: `source .venv/bin/activate`.

## Build

```powershell
python main.py --websites-folder websites --build-websites                  # every website of websites/
python main.py --websites-folder websites --build-websites pamela    # only pamela, the others are left as they are
python main.py --websites-folder examples\demo\components\websites --build-websites    # the demo
```

Every version a website declares is cloned from git and built. The websites are in `websites/build`,
each in the folder of its `site_url` (`build/pamela/docs/`): the latest version at its root, each earlier
version in a folder named after it.

To look at it, serve that folder with any web server, for example
`python -m http.server 8000 --directory websites\build`, then open http://localhost:8000/pamela/docs/.
For the demo: `python -m http.server 8000 --directory examples\demo\components\websites\build`.

The demo in `examples/demo/components` (its `websites/` folder) does all of this with Gradle:

```powershell
./gradlew buildDocumentationSites                      # every website (-Pwebsites=pamela,connie to build one site)
./gradlew serveDocumentationSites                      # http://localhost:8000
```

## Search

The search of a website covers the latest version of every website built in `websites/build`.

## Settings

| Key | Role |
|---|---|
| `site_name` | Name of the website |
| `site_description` | One sentence describing the project |
| `site_url` | Address where the website is published. The latest version is served there, the others in `site_url/<name>/`. Its path is the folder of the website in `websites/build` |
| `theme.logo` | Logo of the website: a path inside the website, or an address |
| `extra.repository_url` | The git repository to clone |
| `extra.versions` | The versions to build. For each one: `name` (shown in the menu, used as folder name), `git_ref` (a branch or a tag), `is_latest: true` (on exactly one version) and an optional `navigation` (the menu; without it the menu is generated from the pages) |
| `extra.documentation_sources` | The folders of the repository copied into the website. `source` is relative to the repository root, `destination` is the folder in the website (`.` for its root). A later entry overwrites an earlier one |
| `extra.homepage` | Home page of the project. Its path completes the URLs starting with `/` that lead outside the website (`/javadoc/...` becomes `/<path>/javadoc/...`) |
| `extra.navbar_links` | The links of the top bar |

## Structure of the tool

```text
Zensical-WebBuilder/
├── main.py                              Builds the websites named by --build-websites, or all of them
├── requirements.txt                     Python dependencies
├── CHANGELOG.md
├── examples/
│   ├── website_settings.yml             Template for a project
│   └── demo/components/                 Demo: websites/ (Pamela, Connie) and build.gradle
├── shared/                              Common to every website
│   ├── default_settings.yml             Common settings every website starts from
│   ├── html_templates/                  Overrides of the theme pages
│   │   ├── main.html                    Around each page: breadcrumb, version badge, "no longer maintained" banner, Previous / Next
│   │   └── partials/                    header, navbar_links, version_menu, copyright
│   └── style_and_icon/                  site_style.css and favicon.ico
└── webbuilder/                          The code
    ├── shared_paths.py                  Locations of the files of shared/
    ├── settings/
    │   ├── website_settings.py          Reads website_settings.yml over the shared settings and checks it
    │   ├── website_version.py           One declared version: name, git reference, latest or not, menu; checked
    │   └── website_version_catalog.py   The versions: checks them together, gives each one its folder and address
    ├── scanning/
    │   └── scan_website.py              Finds the websites of websites/ and checks the names asked
    ├── helper/
    │   └── folder_helper.py             Copies and deletes folders (the only use of shutil)
    ├── repository/
    │   └── git_repository.py            Clones a branch or a tag
    ├── preparation/                     Converts a clone to a structure read by Zensical
    │   ├── zensical_input.py            Copies the sources, then writes the menu of versions and Zensical config
    │   ├── page_url_rewriter.py         Rewrites the URLs starting with "/" in the pages
    │   └── page_url_resolver.py         Decides what one such URL becomes
    └── building/
        ├── version_build.py             One version: clone, preparation, Zensical
        ├── website_build.py             All versions of one website, assembled in its folder of websites/build
        └── merge_search_index.py        Gives the search of each website the pages of all the websites
```

After building, a `preparation` folder is created next to each `website_settings.yml`:

```text
preparation/
└── version_builds/<version>/          Kept after the build to see what Zensical was given and produced
    ├── zensical_input/                Sources copied and rewritten
    ├── zensical_config.yml            Configuration given to Zensical
    └── version_site/                  Site built by Zensical (the clone is deleted)
```

## Good to know

- The build reads git.
- Links starting with `/` that lead to a file of the documentation are made relative in the build; the
  Markdown of your repository is not changed.
- A build that fails keeps the previous website.
- The search links between websites are relative: deploy `websites/build` as it is, so the websites stay side by side.
