from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QSpinBox, QDoubleSpinBox, QDialog, QFormLayout, QDialogButtonBox, QDateEdit, QMessageBox
from PyQt5.QtCore import QDate, Qt
from ...services.inventory import InventoryService


class ProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Product")
        form = QFormLayout(self)
        self.name = QLineEdit(); self.name.setPlaceholderText("Name")
        self.barcode = QLineEdit(); self.barcode.setPlaceholderText("Barcode (optional)")
        self.category = QLineEdit(); self.category.setPlaceholderText("Category")
        self.cost = QDoubleSpinBox(); self.cost.setMaximum(1e9); self.cost.setPrefix("$ "); self.cost.setDecimals(2)
        self.price = QDoubleSpinBox(); self.price.setMaximum(1e9); self.price.setPrefix("$ "); self.price.setDecimals(2)
        self.qty = QSpinBox(); self.qty.setMaximum(1_000_000)
        self.reorder = QSpinBox(); self.reorder.setMaximum(1_000)
        self.expiry = QDateEdit(); self.expiry.setCalendarPopup(True)
        self.expiry.setDate(QDate.currentDate())
        form.addRow("Name", self.name)
        form.addRow("Barcode", self.barcode)
        form.addRow("Category", self.category)
        form.addRow("Cost Price", self.cost)
        form.addRow("Unit Price", self.price)
        form.addRow("Quantity", self.qty)
        form.addRow("Reorder Level", self.reorder)
        form.addRow("Expiry Date", self.expiry)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)


class InventoryPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        top = QHBoxLayout()
        self.search = QLineEdit(); self.search.setPlaceholderText("Search by name, category, barcode")
        add_btn = QPushButton("Add Product")
        refresh_btn = QPushButton("Refresh")
        top.addWidget(self.search)
        top.addWidget(refresh_btn)
        top.addWidget(add_btn)

        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels(["Name", "Barcode", "Category", "Cost", "Price", "Qty", "Expiry"])

        layout.addLayout(top)
        layout.addWidget(self.table)

        refresh_btn.clicked.connect(self.refresh)
        add_btn.clicked.connect(self.add_product)
        self.search.textChanged.connect(lambda: self.refresh())

        self.refresh()

    def refresh(self):
        products = InventoryService.list_products(search=self.search.text().strip() or None)
        self.table.setRowCount(len(products))
        for r, p in enumerate(products):
            self.table.setItem(r, 0, QTableWidgetItem(p.name))
            self.table.setItem(r, 1, QTableWidgetItem(p.barcode or ""))
            self.table.setItem(r, 2, QTableWidgetItem(p.category or ""))
            self.table.setItem(r, 3, QTableWidgetItem(f"{p.cost_price:.2f}"))
            self.table.setItem(r, 4, QTableWidgetItem(f"{p.unit_price:.2f}"))
            qty_item = QTableWidgetItem(str(p.quantity))
            if p.quantity <= p.reorder_level:
                qty_item.setBackground(Qt.yellow)
            self.table.setItem(r, 5, qty_item)
            self.table.setItem(r, 6, QTableWidgetItem(p.expiry_date or ""))

    def add_product(self):
        dlg = ProductDialog(self)
        if dlg.exec_() == QDialog.Accepted:
            if not dlg.name.text().strip():
                QMessageBox.warning(self, "Validation", "Name is required")
                return
            InventoryService.add_product(
                name=dlg.name.text().strip(),
                unit_price=float(dlg.price.value()),
                cost_price=float(dlg.cost.value()),
                quantity=int(dlg.qty.value()),
                barcode=dlg.barcode.text().strip() or None,
                category=dlg.category.text().strip() or None,
                reorder_level=int(dlg.reorder.value()),
                expiry_date=dlg.expiry.date().toString("yyyy-MM-dd"),
            )
            self.refresh()