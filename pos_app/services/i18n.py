from PyQt5.QtCore import QLibraryInfo, QTranslator, QLocale
from PyQt5.QtWidgets import QApplication


class TranslatorService:
    @staticmethod
    def install_qt_translator(app: QApplication, translator: QTranslator, locale_name: str) -> None:
        qt_translator = QTranslator(app)
        qt_path = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
        locale = QLocale(locale_name)
        qt_translator.load(locale, 'qtbase', '_', qt_path)
        app.installTranslator(qt_translator)
        # App translator stub (for future .qm files)
        if translator and locale_name:
            # Would load app-specific .qm here
            pass