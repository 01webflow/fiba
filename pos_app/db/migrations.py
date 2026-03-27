import argparse
import os
import sqlite3
from .database import get_connection, ensure_dirs, DB_PATH

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')


def initialize_database(db_path: str = DB_PATH):
    ensure_dirs()
    with get_connection(db_path) as conn:
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            sql = f.read()
        conn.executescript(sql)
        conn.commit()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--init', action='store_true', help='Initialize database schema')
    parser.add_argument('--db', type=str, default=DB_PATH, help='Path to sqlite database file')
    args = parser.parse_args()
    if args.init:
        initialize_database(args.db)
        print(f"Initialized database at {args.db}")


if __name__ == '__main__':
    main()