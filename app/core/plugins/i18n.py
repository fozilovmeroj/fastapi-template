from pathlib import Path

import i18n

import app.core.config as config


def init_i18n() -> None:
    """
    Initializes i18n, sets needed configs
    """
    lang_path = Path("lang")

    # Recursively add all folders under lang/ to i18n.load_path
    for path in lang_path.glob("**/"):
        if path.is_dir():
            i18n.load_path.append(path)

    i18n.load_path.append("lang")
    i18n.set("locale", config.LOCALE)
    i18n.set('filename_format', '{locale}.{format}')
    i18n.set("fallback", "en")
    i18n.set("skip_locale_root_data", True)


def change_locale(locale: str) -> None:
    i18n.set('locale', locale)
