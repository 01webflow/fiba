import os
import sqlite3
from typing import Optional

APP_DIR = os.path.join(os.path.expanduser("~"), ".pixar_pos")
DATA_DIR = os.path.join(APP_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "pos.db")
BACKUP_DIR = os.path.join(APP_DIR, "backups")


def ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)


def get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    ensure_dirs()
    path = db_path or DB_PATH
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn