# Website builder

Builds a documentation website from the Markdown of a repository, with [Zensical](https://zensical.org).
Needs Python 3.11 to 3.13 (3.14 and later: PyYAML and Zensical do not install yet).

## Structure

```
website_settings.yml        belongs to each repository: name, menu, links, Markdown folders, previous versions

Zensical-WebBuilder/        the tool, the same for every repository
├─ prepare_website_build.py
├─ merge_search_indexes.py
├─ requirements.txt
├─ webbuilder/
│  ├─ website_settings.py      WebsiteSettings: shared settings completed by the project's
│  ├─ website_input.py         WebsiteInput: input folder and config read by Zensical
│  └─ search_index.py          SearchIndex: search.json, with the pages of other websites
├─ shared/
│  ├─ site_settings.yml        theme, footer
│  ├─ html_templates/
│  └─ style_and_icon/
└─ examples/
   └─ website_settings.yml     template to copy for a new repository

build/website/              generated: input/, zensical_config.yml, output/ (the website)
```

To document another repository, copy `examples/website_settings.yml`, adapt it and run the same tool.

## Build

```bash
./gradlew buildDocumentationSite
```

The website is written to `build/website/output`.

## Preview

From the tool folder. Run the 4th command again after editing a Markdown file.

```powershell
python -m venv .venv                                # once
.venv\Scripts\Activate.ps1                          # each terminal (Linux, macOS: source .venv/bin/activate)
pip install -r requirements.txt                     # once
python prepare_website_build.py --settings ../pamela_website/website_settings.yml --build-folder ../build/website
zensical serve -f ../build/website/zensical_config.yml
```

Open http://localhost:8000. Without `--version` the navbar shows "dev".

## Global search

The search box of a website can also find the pages of the other Openflexo websites. Declare them
in `website_settings.yml` (see `examples/website_settings.yml`), then, after `zensical build`:

```bash
python merge_search_indexes.py --settings <website_settings.yml> --build-folder <folder>
```

The `search.json` of the other websites is downloaded when the script runs. A website that cannot be
reached is skipped with a warning.

Limitation: the websites must share the same domain (for example `openflexo.org/pamela/docs/` and
`openflexo.org/connie/docs/`). The search box opens its results relative to the current website, so
a website on another domain is skipped with a warning.

## Versions

The version menu reads `versions.json`: the current version (`--version`, which Gradle sets from
the project version), then the `previous_versions` of `website_settings.yml`. Previous versions are
not rebuilt, the menu links to where they are published.
