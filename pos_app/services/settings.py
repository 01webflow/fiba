from typing import Optional
from ..db.database import get_connection


class SettingsService:
    @staticmethod
    def ensure_app_dirs():
        from ..db.database import ensure_dirs  # local import to avoid cycles
        ensure_dirs()

    @staticmethod
    def get_setting(key: str, default: Optional[str] = None) -> Optional[str]:
        with get_connection() as conn:
            cur = conn.execute("SELECT value FROM settings WHERE key = ?", (key,))
            row = cur.fetchone()
            return row[0] if row else default

    @staticmethod
    def set_setting(key: str, value: str) -> None:
        with get_connection() as conn:
            conn.execute("INSERT INTO settings(key, value) VALUES(?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key, value))
            conn.commit()