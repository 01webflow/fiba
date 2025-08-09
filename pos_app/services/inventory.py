from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional
from ..db.database import get_connection


@dataclass
class Product:
    id: int
    name: str
    barcode: Optional[str]
    category: Optional[str]
    cost_price: float
    unit_price: float
    quantity: int
    reorder_level: int
    expiry_date: Optional[str]
    created_at: Optional[str] = None


class InventoryService:
    @staticmethod
    def add_product(name: str, unit_price: float, cost_price: float, quantity: int = 0, barcode: Optional[str] = None, category: Optional[str] = None, reorder_level: int = 5, expiry_date: Optional[str] = None) -> int:
        with get_connection() as conn:
            cur = conn.execute(
                "INSERT INTO products(name, barcode, category, cost_price, unit_price, quantity, reorder_level, expiry_date) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                (name, barcode, category, cost_price, unit_price, quantity, reorder_level, expiry_date),
            )
            conn.commit()
            return cur.lastrowid

    @staticmethod
    def update_quantity(product_id: int, delta: int) -> None:
        with get_connection() as conn:
            conn.execute("UPDATE products SET quantity = quantity + ? WHERE id = ?", (delta, product_id))
            conn.commit()

    @staticmethod
    def get_product_by_barcode(barcode: str) -> Optional[Product]:
        with get_connection() as conn:
            cur = conn.execute("SELECT * FROM products WHERE barcode = ?", (barcode,))
            row = cur.fetchone()
            return Product(**row) if row else None

    @staticmethod
    def list_products(search: Optional[str] = None) -> List[Product]:
        with get_connection() as conn:
            if search:
                like = f"%{search}%"
                cur = conn.execute(
                    "SELECT * FROM products WHERE name LIKE ? OR category LIKE ? OR barcode LIKE ? ORDER BY name",
                    (like, like, like),
                )
            else:
                cur = conn.execute("SELECT * FROM products ORDER BY name")
            return [Product(**row) for row in cur.fetchall()]

    @staticmethod
    def low_stock(threshold: int = 0) -> List[Product]:
        with get_connection() as conn:
            cur = conn.execute("SELECT * FROM products WHERE quantity <= COALESCE(NULLIF(?, 0), reorder_level)", (threshold,))
            return [Product(**row) for row in cur.fetchall()]

    @staticmethod
    def expiring_soon(days: int = 30) -> List[Product]:
        cutoff = (datetime.utcnow() + timedelta(days=days)).strftime("%Y-%m-%d")
        with get_connection() as conn:
            cur = conn.execute("SELECT * FROM products WHERE expiry_date IS NOT NULL AND expiry_date <= ?", (cutoff,))
            return [Product(**row) for row in cur.fetchall()]