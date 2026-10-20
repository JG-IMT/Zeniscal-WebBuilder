from pathlib import Path

SHARED_FOLDER: Path = Path(__file__).resolve().parents[1] / "shared"
DEFAULT_SETTINGS_FILE: Path = SHARED_FOLDER / "default_settings.yml"
SHARED_STYLE_AND_ICON_FOLDER: Path = SHARED_FOLDER / "style_and_icon"
SHARED_HTML_TEMPLATES_FOLDER: Path = SHARED_FOLDER / "html_templates"
