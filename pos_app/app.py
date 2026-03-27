from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTranslator, QLocale
from .services.settings import SettingsService
from .services.i18n import TranslatorService
from .ui.styles.loader import StyleLoader


def create_app() -> QApplication:
    app = QApplication.instance() or QApplication([])
    app.setApplicationName("Pixar POS")

    # Settings
    SettingsService.ensure_app_dirs()

    # Translations (default locale)
    translator = QTranslator()
    lang = SettingsService.get_setting("language", QLocale.system().name())
    TranslatorService.install_qt_translator(app, translator, lang)

    # Styles
    theme = SettingsService.get_setting("theme", "glass")
    StyleLoader.apply_theme(app, theme)

    return app