import math
from pos_app.services.billing import BillingService, CartItem
from pos_app.db.migrations import initialize_database
from pos_app.db.database import DB_PATH
import os


def setup_module(module):
    # Fresh DB
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    initialize_database(DB_PATH)
    # Seed exchange rate for EUR
    from pos_app.db.database import get_connection
    with get_connection() as conn:
        conn.execute("INSERT INTO exchange_rates(currency, rate_to_usd) VALUES('EUR', 0.9)")
        conn.commit()


def test_totals_usd():
    items = [
        CartItem(product_id=1, name='Coffee', quantity=2, unit_price=3.50),
        CartItem(product_id=2, name='Bagel', quantity=1, unit_price=2.00),
    ]
    totals = BillingService.calculate_totals(items, discount_pct=10.0, tax_pct=5.0, currency='USD')
    assert math.isclose(totals.subtotal, 9.0, rel_tol=1e-5)
    assert math.isclose(totals.discount, 0.9, rel_tol=1e-5)
    assert math.isclose(totals.tax, 0.405, rel_tol=1e-5)
    assert math.isclose(totals.total, 8.505, rel_tol=1e-5)


def test_totals_eur_conversion():
    items = [CartItem(product_id=1, name='Item', quantity=1, unit_price=10.0)]
    totals = BillingService.calculate_totals(items, discount_pct=0.0, tax_pct=0.0, currency='EUR')
    assert math.isclose(totals.subtotal, 9.0, rel_tol=1e-5)
    assert totals.currency == 'EUR'