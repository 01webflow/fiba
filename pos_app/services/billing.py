from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
from ..db.database import get_connection


@dataclass
class CartItem:
    product_id: int
    name: str
    quantity: int
    unit_price: float

    @property
    def total(self) -> float:
        return round(self.quantity * self.unit_price, 2)


@dataclass
class CartTotals:
    subtotal: float
    discount: float
    tax: float
    total: float
    currency: str


class CurrencyService:
    @staticmethod
    def get_rate(currency: str) -> float:
        if currency.upper() == 'USD':
            return 1.0
        with get_connection() as conn:
            cur = conn.execute("SELECT rate_to_usd FROM exchange_rates WHERE currency = ?", (currency.upper(),))
            row = cur.fetchone()
            if not row:
                raise ValueError("Unknown currency")
            return float(row[0])

    @staticmethod
    def convert_from_usd(amount: float, currency: str) -> float:
        rate = CurrencyService.get_rate(currency)
        return round(amount * rate, 2)


class BillingService:
    @staticmethod
    def calculate_totals(items: List[CartItem], discount_pct: float = 0.0, tax_pct: float = 0.0, currency: str = 'USD') -> CartTotals:
        subtotal_usd = round(sum(i.total for i in items), 2)
        discount_usd = round(subtotal_usd * (discount_pct / 100.0), 2)
        taxed_base_usd = subtotal_usd - discount_usd
        tax_usd = round(taxed_base_usd * (tax_pct / 100.0), 3)
        total_usd = round(taxed_base_usd + tax_usd, 3)
        if currency.upper() != 'USD':
            subtotal = CurrencyService.convert_from_usd(subtotal_usd, currency)
            discount = CurrencyService.convert_from_usd(discount_usd, currency)
            tax = CurrencyService.convert_from_usd(tax_usd, currency)
            total = CurrencyService.convert_from_usd(total_usd, currency)
        else:
            subtotal, discount, tax, total = subtotal_usd, discount_usd, tax_usd, total_usd
        return CartTotals(subtotal, discount, tax, total, currency.upper())

    @staticmethod
    def persist_sale(user_id: int, items: List[CartItem], totals: CartTotals, customer_id: Optional[int] = None) -> int:
        with get_connection() as conn:
            cur = conn.execute(
                "INSERT INTO sales(user_id, customer_id, subtotal, discount, tax, total, currency) VALUES(?, ?, ?, ?, ?, ?, ?)",
                (user_id, customer_id, totals.subtotal, totals.discount, totals.tax, totals.total, totals.currency),
            )
            sale_id = cur.lastrowid
            for item in items:
                conn.execute(
                    "INSERT INTO sale_items(sale_id, product_id, quantity, unit_price, total_price) VALUES(?, ?, ?, ?, ?)",
                    (sale_id, item.product_id, item.quantity, item.unit_price, item.total),
                )
                conn.execute("UPDATE products SET quantity = quantity - ? WHERE id = ?", (item.quantity, item.product_id))
            conn.commit()
            return sale_id