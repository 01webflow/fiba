from typing import Optional
from ..db.database import get_connection


def log_action(user_id: Optional[int], action: str, details: Optional[str] = None) -> None:
    with get_connection() as conn:
        conn.execute("INSERT INTO audit_logs(user_id, action, details) VALUES(?, ?, ?)", (user_id, action, details))
        conn.commit()