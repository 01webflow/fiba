from PyQt5.QtWidgets import QApplication
from .app import create_app
from .ui.login_window import LoginWindow


def main():
    app: QApplication = create_app()
    window = LoginWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()