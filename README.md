# PyQt POS System

Quick start:

- Create venv and install dependencies:
  - python -m venv .venv && source .venv/bin/activate
  - pip install -r requirements.txt
- Initialize database and demo data:
  - python -m pos_app.db.migrations --init
  - python scripts/seed.py
- Run the app:
  - python -m pos_app.main
- Run tests:
  - pytest -q

Demo logins:
- admin@example.com / Admin@123 (role: Super Admin)
- cashier@example.com / Cashier@123 (role: Cashier)