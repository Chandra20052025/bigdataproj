import pandas as pd
import random
import time
import json
import os
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)


def random_date(days_back: int = 90) -> str:
    """Return a random date within the last N days as YYYY-MM-DD."""
    delta = timedelta(days=random.randint(0, days_back))
    return (datetime.now() - delta).strftime("%Y-%m-%d")


def init_csv_if_missing():
    """Create empty CSVs with proper headers if they don't exist."""
    sales_path = f"{DATA_DIR}/sales.csv"
    if not os.path.exists(sales_path):
        pd.DataFrame(columns=[
            "id", "date", "department", "month", "region",
            "product", "quantity", "amount", "customer", "sales_person"
        ]).to_csv(sales_path, index=False)

    hr_path = f"{DATA_DIR}/hr.csv"
    if not os.path.exists(hr_path):
        pd.DataFrame(columns=[
            "id", "date", "department", "month", "employee_name",
            "role", "salary", "experience", "location"
        ]).to_csv(hr_path, index=False)

    finance_path = f"{DATA_DIR}/finance.csv"
    if not os.path.exists(finance_path):
        pd.DataFrame(columns=[
            "id", "date", "department", "month", "expense_type",
            "amount", "vendor", "approved_by"
        ]).to_csv(finance_path, index=False)

    prod_path = f"{DATA_DIR}/production.json"
    if not os.path.exists(prod_path):
        with open(prod_path, "w") as f:
            json.dump([], f)


def generate_row():
    """Generate one row for each department and append to data files."""

    record_date = random_date(days_back=90)
    month = record_date[:7]  # YYYY-MM

    # ── SALES ────────────────────────────────────────────────────────────────
    sales_df = pd.read_csv(f"{DATA_DIR}/sales.csv")
    sales_row = {
        "id": len(sales_df) + 1,
        "date": record_date,
        "department": "Sales",
        "month": month,
        "region": random.choice(["North", "South", "East", "West"]),
        "product": random.choice(["Laptop", "Phone", "Tablet", "Monitor", "Server"]),
        "quantity": random.randint(1, 20),
        "amount": random.randint(10000, 120000),
        "customer": fake.company(),
        "sales_person": fake.name(),
    }
    sales_df.loc[len(sales_df)] = sales_row
    sales_df.to_csv(f"{DATA_DIR}/sales.csv", index=False)

    # ── HR ───────────────────────────────────────────────────────────────────
    hr_df = pd.read_csv(f"{DATA_DIR}/hr.csv")
    hr_row = {
        "id": len(hr_df) + 1,
        "date": record_date,
        "department": "HR",
        "month": month,
        "employee_name": fake.name(),
        "role": random.choice(["Manager", "Engineer", "Analyst", "Designer", "DevOps"]),
        "salary": random.randint(30000, 140000),
        "experience": random.randint(1, 15),
        "location": fake.city(),
    }
    hr_df.loc[len(hr_df)] = hr_row
    hr_df.to_csv(f"{DATA_DIR}/hr.csv", index=False)

    # ── FINANCE ──────────────────────────────────────────────────────────────
    finance_df = pd.read_csv(f"{DATA_DIR}/finance.csv")
    finance_row = {
        "id": len(finance_df) + 1,
        "date": record_date,
        "department": "Finance",
        "month": month,
        "expense_type": random.choice(["Cloud", "Software", "Tax", "Operations", "Marketing"]),
        "amount": random.randint(5000, 90000),
        "vendor": fake.company(),
        "approved_by": fake.name(),
    }
    finance_df.loc[len(finance_df)] = finance_row
    finance_df.to_csv(f"{DATA_DIR}/finance.csv", index=False)

    # ── PRODUCTION ───────────────────────────────────────────────────────────
    with open(f"{DATA_DIR}/production.json", "r") as f:
        production_data = json.load(f)

    production_row = {
        "id": len(production_data) + 1,
        "date": record_date,
        "department": "Production",
        "month": month,
        "factory": random.choice(["Plant-A", "Plant-B", "Plant-C"]),
        "units_produced": random.randint(100, 2000),
        "cost": random.randint(10000, 150000),
        "manager": fake.name(),
    }
    production_data.append(production_row)

    with open(f"{DATA_DIR}/production.json", "w") as f:
        json.dump(production_data, f, indent=2)

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Row added — date: {record_date}")


if __name__ == "__main__":
    print("LIVE DATA GENERATOR STARTED — Ctrl+C to stop")
    init_csv_if_missing()

    # Seed 100 historical rows on first run so filters have data to work with
    existing = 0
    try:
        existing = len(pd.read_csv(f"{DATA_DIR}/sales.csv"))
    except Exception:
        pass

    if existing < 10:
        print("Seeding 100 historical rows...")
        for _ in range(100):
            generate_row()
        print("Seeding complete.")

    while True:
        generate_row()
        time.sleep(5)