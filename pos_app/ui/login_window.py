from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QComboBox, QMessageBox
from PyQt5.QtCore import Qt
from ..services import auth
from ..services.audit import log_action
from .main_window import MainWindow


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pixar POS - Login")
        self.setObjectName("GlassCard")
        self.resize(420, 320)

        layout = QVBoxLayout(self)
        title = QLabel("Pixar POS")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: 600;")

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)

        # Signup fields
        self.name = QLineEdit()
        self.name.setPlaceholderText("Full name (for signup)")
        self.role = QComboBox()
        for r in auth.ROLES:
            self.role.addItem(r)

        buttons = QHBoxLayout()
        self.login_btn = QPushButton("Login")
        self.signup_btn = QPushButton("Sign up")
        self.login_btn.clicked.connect(self.handle_login)
        self.signup_btn.clicked.connect(self.handle_signup)
        buttons.addWidget(self.login_btn)
        buttons.addWidget(self.signup_btn)

        layout.addWidget(title)
        layout.addWidget(self.email)
        layout.addWidget(self.password)
        layout.addWidget(self.name)
        layout.addWidget(self.role)
        layout.addLayout(buttons)

    def handle_login(self):
        creds = auth.login(self.email.text().strip(), self.password.text())
        if creds:
            user_id, name, role = creds
            log_action(user_id, "login", f"Role={role}")
            self.hide()
            self.main = MainWindow(user_id=user_id, user_name=name, role=role)
            self.main.show()
        else:
            QMessageBox.warning(self, "Login failed", "Invalid credentials")

    def handle_signup(self):
        try:
            user_id = auth.signup(
                email=self.email.text().strip(),
                name=self.name.text().strip() or "New User",
                password=self.password.text(),
                role_name=self.role.currentText(),
            )
            QMessageBox.information(self, "Signup", "Account created. You can login now.")
            log_action(user_id, "signup")
        except Exception as e:
            QMessageBox.warning(self, "Signup failed", str(e))