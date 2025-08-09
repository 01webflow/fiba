from pos_app.db.migrations import initialize_database
from pos_app.services.auth import ensure_roles, signup
from pos_app.db.database import get_connection, DB_PATH
from pos_app.services.inventory import InventoryService
import os


def main():
    if not os.path.exists(DB_PATH):
        initialize_database(DB_PATH)
    ensure_roles()

    # Create demo users if not exist
    with get_connection() as conn:
        cur = conn.execute("SELECT COUNT(1) FROM users")
        count = cur.fetchone()[0]
        if count == 0:
            signup("admin@example.com", "Super Admin", "Admin@123", role_name="Super Admin")
            signup("cashier@example.com", "Cashier One", "Cashier@123", role_name="Cashier")

    # Seed products
    with get_connection() as conn:
        cur = conn.execute("SELECT COUNT(1) FROM products")
        if cur.fetchone()[0] == 0:
            InventoryService.add_product("Coffee", 3.5, 1.0, quantity=50, barcode="111", category="Beverage", reorder_level=10)
            InventoryService.add_product("Bagel", 2.0, 0.8, quantity=30, barcode="222", category="Bakery", reorder_level=10)
            InventoryService.add_product("Milk", 1.5, 1.0, quantity=20, barcode="333", category="Dairy", reorder_level=10)

    print("Seeded demo data.")


if __name__ == '__main__':
    main()