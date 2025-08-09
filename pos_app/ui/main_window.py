from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget
from PyQt5.QtCore import Qt
from .widgets.sales_page import SalesPage
from .widgets.inventory_page import InventoryPage
from ..services.settings import SettingsService
from ..ui.styles.loader import StyleLoader


class MainWindow(QMainWindow):
    def __init__(self, user_id: int, user_name: str, role: str):
        super().__init__()
        self.user_id = user_id
        self.user_name = user_name
        self.role = role
        self.setWindowTitle(f"Pixar POS - {user_name} ({role})")
        self.resize(1100, 720)

        container = QWidget()
        self.setCentralWidget(container)
        root = QHBoxLayout(container)

        # Sidebar
        sidebar = QVBoxLayout()
        title = QLabel("Menu")
        title.setStyleSheet("font-size:18px;font-weight:600")
        btn_sales = QPushButton("Sales")
        btn_inventory = QPushButton("Inventory")
        btn_theme = QPushButton("Toggle Theme")
        sidebar.addWidget(title)
        sidebar.addWidget(btn_sales)
        sidebar.addWidget(btn_inventory)
        sidebar.addStretch(1)
        sidebar.addWidget(btn_theme)

        # Pages
        self.stack = QStackedWidget()
        self.sales_page = SalesPage(user_id=self.user_id)
        self.inventory_page = InventoryPage()
        self.stack.addWidget(self.sales_page)
        self.stack.addWidget(self.inventory_page)

        root.addLayout(sidebar, 1)
        root.addWidget(self.stack, 4)

        btn_sales.clicked.connect(lambda: self.stack.setCurrentWidget(self.sales_page))
        btn_inventory.clicked.connect(lambda: self.stack.setCurrentWidget(self.inventory_page))
        btn_theme.clicked.connect(self.toggle_theme)

    def toggle_theme(self):
        current = SettingsService.get_setting("theme", "glass")
        new_theme = "dark" if current != "dark" else "glass"
        SettingsService.set_setting("theme", new_theme)
        StyleLoader.apply_theme(self.app(), new_theme)

    def app(self):
        from PyQt5.QtWidgets import QApplication
        return QApplication.instance()