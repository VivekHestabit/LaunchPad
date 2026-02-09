import sqlite3
import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sales.db")
CSV_PATH = os.path.join(BASE_DIR, "sales.csv")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    customer_id TEXT,
    first_name TEXT,
    last_name TEXT,
    company TEXT,
    city TEXT,
    country TEXT,
    phone_1 TEXT,
    phone_2 TEXT,
    email TEXT,
    subscription_date TEXT,
    website TEXT
)
""")

cursor.execute("DELETE FROM customers")

inserted = 0

with open(CSV_PATH, newline="", encoding="utf-8-sig") as csvfile:
    reader = csv.DictReader(csvfile)

    required_columns = {
        "Index", "Customer Id", "First Name", "Last Name", "Company",
        "City", "Country", "Phone 1", "Phone 2", "Email",
        "Subscription Date", "Website"
    }

    if not required_columns.issubset(reader.fieldnames):
        raise ValueError(f"CSV columns mismatch. Found: {reader.fieldnames}")

    for row in reader:
        cursor.execute("""
        INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row["Index"],
            row["Customer Id"],
            row["First Name"],
            row["Last Name"],
            row["Company"],
            row["City"],
            row["Country"],
            row["Phone 1"],
            row["Phone 2"],
            row["Email"],
            row["Subscription Date"],
            row["Website"]
        ))
        inserted += 1

conn.commit()
conn.close()

print(f"Loaded {inserted} rows into sales.db (customers table)")
