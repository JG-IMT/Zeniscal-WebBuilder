# Known issues and next steps

State on 2026-10-15. Both repositories were clean (everything committed) at the end of the session.

## Environment

- **Python 3.14 and later do not work**: PyYAML and Zensical do not install. Use 3.12.
- **Gradle takes `python` from the PATH.** With 3.15 as the default and no `zensical_website_builder/.venv`,
  `createDocumentationEnvironment` creates a 3.15 environment and the installation fails. Workaround:
  create `.venv` with 3.12 first. Planned: a `documentationPython` property in
  `~/.gradle/gradle.properties`.
- **Gradle needs a JDK** (a JRE alone fails on `compileJava`). JDK 8 (Temurin) is installed.
- **Gradle 8.14 warns** that running on Java 16 or lower will fail in Gradle 9, and about
  `url uri(...)` in the original `buildscript` of Pamela (lines 68 and 79). Not ours.
- **PowerShell blocks `.venv\Scripts\Activate.ps1`**: run
  `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in the terminal, or call
  `.venv\Scripts\python.exe` directly.
- **Windows long paths**: `git worktree add` fails in deep folders. Use `git -c core.longpaths=true ...`.

## Tool

- **No automated tests.** Checks are done by hand on the Pamela sites.
- **`main.py search` is not idempotent**: running it twice on the same `build/output` adds the
  entries twice. Run it right after `zensical build`.
- **Global search**: websites on the same domain only; an unreachable one is skipped with a warning
  (this path was never run). Not wired to Pamela (no `global_search` declared). Pages of the other
  websites are those published at the last build; a targeted refresh without rebuilding is wanted
  (see below).
- **Links starting with "/"**:
  - a link to a page written as an absolute path (`/getting_started`) is not recognised, only
    targets that exist as files in the website are;
  - a link to another project without prefix of the current one (`/other/...`) is prefixed with the
    current project path;
  - links in inline code are converted too (only fenced code blocks are skipped).
- **Versions menu**:
  - the links of earlier versions are absolute production addresses (`previous_versions`): in a
    local test, clicking leaves the local site;
  - if `--version` is not in `previous_versions`, no entry is marked as current (the badge is right).
- **Earlier versions are not built automatically.** Each one needs its branch, a settings file (menu
  limited to its pages) and a manual assembly. Only `1.6` and `1.5.0.1` have enough Markdown; the
  `1.5.1` and `1.5` branches have one page.
- **Zensical strict mode does not detect broken absolute links** (images missing under a sub-path
  still build without warning).
- **The copy of the tool in Pamela is manual** and can drift: `zensical_website_builder/` must be
  re-copied after each change. Planned: install with `pip` from GitHub with a tag (explanation of
  the procedure still to be given to the user at the end).
- **Publishing is not covered**: the old `scp` to `openflexo.org` is in a commented block of
  Pamela's `build.gradle`.

## Not tested yet

- **Connie**: 7 Markdown pages (`src/site/markdown`, `connie-core`, `connie-utils`). Links to
  `/connie/javadoc/...` are left unchanged by the rule. The first line of both `index.md`,
  `[/images/components/connie/ConnieScreenshot] Connie`, is not valid Markdown (content problem
  of Connie); two pages have no `#` title, so `nav` must give the titles; no logo (check that the
  theme accepts a site without `theme.logo`).
- The look of the earlier-version banner in the light theme was checked by its colours only.

## Next steps

1. **Single build for all versions, two Gradle commands** (design validated, not coded):
   `buildDocumentationSite` and `serveDocumentationSite`. A `main.py build` command builds the
   latest version and each earlier version that has a `source` folder, runs Zensical itself, and
   assembles `build/output/<version>/`; `main.py serve` serves that folder. Relative menu links
   for locally built versions. Still to decide: where the imported earlier versions live
   (`pamela_website/versions/` in the repository, or outside it for the demo).
2. **Targeted refresh of the global search** when another website is rebuilt, without rebuilding
   the others (their built output must be kept).
3. **Test the tool on Connie**, with a `website_settings.yml` outside its repository first.
4. **Publishing** and the migration from the copy to `pip` with a tag.
