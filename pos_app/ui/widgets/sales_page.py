from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QSpinBox, QMessageBox
from PyQt5.QtCore import Qt
from ...services.inventory import InventoryService
from ...services.billing import BillingService, CartItem
from ...services.pdf import generate_invoice_pdf
from ...services.audit import log_action
import os


class SalesPage(QWidget):
    def __init__(self, user_id: int):
        super().__init__()
        self.user_id = user_id
        self.items = []
        layout = QVBoxLayout(self)

        top = QHBoxLayout()
        self.search = QLineEdit(); self.search.setPlaceholderText("Scan barcode or type product name")
        self.qty = QSpinBox(); self.qty.setRange(1, 999); self.qty.setValue(1)
        add_btn = QPushButton("Add")
        top.addWidget(self.search)
        top.addWidget(self.qty)
        top.addWidget(add_btn)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Product", "Qty", "Unit Price", "Total"])\

        bottom = QHBoxLayout()
        self.total_label = QLabel("Total: 0.00 USD")
        checkout_btn = QPushButton("Checkout")
        clear_btn = QPushButton("Clear")
        bottom.addWidget(self.total_label)
        bottom.addStretch(1)
        bottom.addWidget(clear_btn)
        bottom.addWidget(checkout_btn)

        layout.addLayout(top)
        layout.addWidget(self.table)
        layout.addLayout(bottom)

        add_btn.clicked.connect(self.add_item)
        clear_btn.clicked.connect(self.clear_cart)
        checkout_btn.clicked.connect(self.checkout)

    def add_item(self):
        query = self.search.text().strip()
        product = InventoryService.get_product_by_barcode(query)
        if not product:
            # fallback by name contains
            products = InventoryService.list_products(search=query)
            product = products[0] if products else None
        if not product:
            QMessageBox.information(self, "Not found", "No matching product")
            return
        qty = self.qty.value()
        item = CartItem(product_id=product.id, name=product.name, quantity=qty, unit_price=product.unit_price)
        self.items.append(item)
        self.refresh_table()
        self.search.clear()
        self.qty.setValue(1)

    def refresh_table(self):
        self.table.setRowCount(len(self.items))
        for r, item in enumerate(self.items):
            self.table.setItem(r, 0, QTableWidgetItem(item.name))
            self.table.setItem(r, 1, QTableWidgetItem(str(item.quantity)))
            self.table.setItem(r, 2, QTableWidgetItem(f"{item.unit_price:.2f}"))
            self.table.setItem(r, 3, QTableWidgetItem(f"{item.total:.2f}"))
        totals = BillingService.calculate_totals(self.items, discount_pct=0.0, tax_pct=7.5, currency='USD')
        self.total_label.setText(f"Total: {totals.total:.2f} {totals.currency}")

    def clear_cart(self):
        self.items = []
        self.refresh_table()

    def checkout(self):
        if not self.items:
            QMessageBox.information(self, "Cart", "Cart is empty")
            return
        totals = BillingService.calculate_totals(self.items, discount_pct=0.0, tax_pct=7.5, currency='USD')
        sale_id = BillingService.persist_sale(self.user_id, self.items, totals)
        out_dir = os.path.join(os.path.expanduser("~"), ".pixar_pos", "invoices")
        os.makedirs(out_dir, exist_ok=True)
        pdf_path = os.path.join(out_dir, f"invoice_{sale_id}.pdf")
        generate_invoice_pdf(pdf_path, sale_id, self.items, totals)
        log_action(self.user_id, "checkout", f"sale_id={sale_id}")
        QMessageBox.information(self, "Sale complete", f"Invoice saved to:\n{pdf_path}")
        self.clear_cart()