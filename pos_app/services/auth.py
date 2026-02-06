from typing import Optional, Tuple
from ..db.database import get_connection
from ..utils.hashing import hash_password, verify_password

ROLES = [
    "Super Admin",
    "Admin",
    "Manager",
    "Assistant Manager",
    "Supervisor",
    "Cashier",
    "Helper",
]


def ensure_roles():
    with get_connection() as conn:
        for role in ROLES:
            conn.execute("INSERT OR IGNORE INTO roles(name) VALUES (?)", (role,))
        conn.commit()


def signup(email: str, name: str, password: str, role_name: str = "Cashier") -> int:
    ensure_roles()
    with get_connection() as conn:
        cur = conn.execute("SELECT id FROM roles WHERE name = ?", (role_name,))
        role = cur.fetchone()
        if not role:
            raise ValueError("Invalid role")
        password_hash = hash_password(password)
        cur = conn.execute(
            "INSERT INTO users(email, name, password_hash, role_id) VALUES(?, ?, ?, ?)",
            (email, name, password_hash, role[0]),
        )
        conn.commit()
        return cur.lastrowid


def login(email: str, password: str) -> Optional[Tuple[int, str, str]]:
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT users.id, users.name, users.password_hash, roles.name as role FROM users JOIN roles ON roles.id = users.role_id WHERE email = ? AND is_active = 1",
            (email,),
        )
        row = cur.fetchone()
        if row and verify_password(password, row[2]):
            conn.execute("INSERT INTO sessions(user_id) VALUES(?)", (row[0],))
            conn.commit()
            return row[0], row[1], row[3]
        return None