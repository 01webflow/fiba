from pos_app.db.migrations import initialize_database
from pos_app.db.database import DB_PATH, get_connection
from pos_app.services.inventory import InventoryService
from datetime import datetime, timedelta
import os


def setup_module(module):
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    initialize_database(DB_PATH)


def test_low_stock_detection():
    pid = InventoryService.add_product(name='Milk', unit_price=1.5, cost_price=1.0, quantity=2, reorder_level=5)
    lows = InventoryService.low_stock()
    assert any(p.id == pid for p in lows)


def test_expiring_soon():
    expiry = (datetime.utcnow() + timedelta(days=5)).strftime('%Y-%m-%d')
    pid = InventoryService.add_product(name='Yogurt', unit_price=2.0, cost_price=1.2, quantity=10, expiry_date=expiry)
    expiring = InventoryService.expiring_soon(days=7)
    assert any(p.id == pid for p in expiring)