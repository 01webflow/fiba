import os
from PyQt5.QtWidgets import QApplication

STYLES_DIR = os.path.join(os.path.dirname(__file__))


def _read_qss(name: str) -> str:
    path = os.path.join(STYLES_DIR, f"{name}.qss")
    if not os.path.exists(path):
        return ""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


class StyleLoader:
    @staticmethod
    def apply_theme(app: QApplication, theme: str = "glass") -> None:
        qss = _read_qss(theme)
        app.setStyleSheet(qss)