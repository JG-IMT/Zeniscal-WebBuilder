# Known issues and next steps

State on 2026-10-19. The tool is ahead of Pamela: Pamela still has the old copy of the tool and the
old `website_settings.yml` (no `versions`), see "Next steps".

## Environment

- **Python**: the tool and Zensical 0.0.70 were run with Python 3.14.6 (PyYAML 6.0.3). The notes of
  2026-10-15 said 3.14 and later did not install; 3.15 was not checked.
- **Gradle takes `python` from the PATH.** With no `zensical_website_builder/.venv`,
  `createDocumentationEnvironment` creates the environment with the default Python. Workaround:
  create `.venv` with a Python that works first. Planned: a `documentationPython` property in
  `~/.gradle/gradle.properties`.
- **Gradle needs a JDK** (a JRE alone fails on `compileJava`). JDK 8 (Temurin) is installed.
- **Gradle 8.14 warns** that running on Java 16 or lower will fail in Gradle 9, and about
  `url uri(...)` in the original `buildscript` of Pamela (lines 68 and 79). Not ours.
- **PowerShell blocks `.venv\Scripts\Activate.ps1`**: run
  `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in the terminal, or call
  `.venv\Scripts\python.exe` directly.

## Tool

- **No automated tests.** Checks are done by hand on clones of Pamela (`1.6.1`, `1.6`, `1.5.0.1`).
- **`build` reads git, not the working folder**: unpushed work is not in the website (use
  `--repository-url <folder>` for committed work).
- **`build` clones every version again** (shallow clone, no cache) and stops at the first version
  that fails: `build/website` is then incomplete.
- **Deleting a clone on Windows** uses the `onerror` option of `shutil.rmtree`, deprecated since
  Python 3.12 (a warning today).
- **Version menu**: the "same page" test asks the server for the page and expects a 404 when it does
  not exist. A server answering 200 with an error page would break it (not checked in production).
- **Search across components is not implemented** (removed on 2026-10-19, not ready for production):
  each version keeps the search of its own pages. To do it later, a site must publish an index of its
  own pages only, so that the sites do not copy each other's entries.
- **Links starting with "/"** are fixed silently:
  - a link to a page written as an absolute path (`/getting_started`) is not recognised, only
    targets that exist as files in the website are;
  - a link to another project without prefix of the current one (`/other/...`) is prefixed with the
    current project path (a guess, nothing reports it);
  - links in inline code are converted too (only fenced code blocks are skipped).
- **Zensical strict mode does not detect broken absolute links** (images missing under a sub-path
  still build without warning).
- **The project path** comes from `homepage` (implicit): changing the home page changes the links.
- **The copy of the tool in Pamela is manual** and can drift. Planned: install with `pip` from GitHub
  with a tag (explanation of the procedure still to be given to the user at the end).
- **Publishing is not covered**: the old `scp` to `openflexo.org` is in a commented block of
  Pamela's `build.gradle`.

## Not tested yet

- **Connie**: 7 Markdown pages (`src/site/markdown`, `connie-core`, `connie-utils`). Links to
  `/connie/javadoc/...` are left unchanged by the rule. The first line of both `index.md`,
  `[/images/components/connie/ConnieScreenshot] Connie`, is not valid Markdown (content problem
  of Connie); two pages have no `#` title, so `navigation` must give the titles; no logo (check that
  the theme accepts a site without `theme.logo`).
- The look of the earlier-version banner in the light theme was checked by its colours only.

## Next steps

1. **Migrate Pamela**: `website_settings.yml` (`repository_url`, `versions` with branches `1.6.1` and
   `1.6` and tag `1.5.0.1`, sources without `../`, the former `nav` as `navigation` of `1.6.1`), Gradle
   tasks calling `main.py build` and `main.py serve`, new copy of the tool.
2. **Tags**: ask the person in charge to tag the releases (`1.6.1`, `1.6`); until then the versions
   are built from branches, which move.
3. **Report the links the build rewrites**, in particular the ones whose target was guessed.
4. **Search across components** (Pamela, Connie, Diana), once the first component is in production.
5. **Test the tool on Connie**, with a `website_settings.yml` outside its repository first.
6. **Publishing** and the migration from the copy to `pip` with a tag.
7. **Automated tests**, starting with `WebsitePathResolver`, `MarkdownPathRewriter` and the checks of `WebsiteSettings`.
