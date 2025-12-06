from pathlib import Path
import i18n

import app.core.config as config


def init_i18n() -> None:
    """
    Initializes i18n, sets needed configs
    """

    i18n.load_path.append("lang")
    i18n.set("locale", config.LOCALE)
    i18n.set("file_format", "yml")
    i18n.set("filename_format", "{namespace}.{format}")
    i18n.set("skip_locale_root_data", True)


def change_locale(locale: str) -> None:
    i18n.set('locale', locale)
