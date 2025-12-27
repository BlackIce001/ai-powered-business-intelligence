import sqlite3
import pandas as pd
from pathlib import Path

# -------------------------
# PROJECT PATHS
# -------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
DB_PATH = PROJECT_ROOT / "data" / "mindone_dw.db"

# -------------------------
# CONNECT TO SQLITE
# -------------------------
conn = sqlite3.connect(DB_PATH)
print("✅ Connected to SQLite database")

# -------------------------
# LOAD DATA
# -------------------------
fact_sales = pd.read_csv(DATA_PROCESSED / "fact_sales.csv")
dim_customers = pd.read_csv(DATA_PROCESSED / "dim_customers.csv")
dim_products = pd.read_csv(DATA_PROCESSED / "dim_products.csv")
dim_sellers = pd.read_csv(DATA_PROCESSED / "dim_sellers.csv")
dim_dates = pd.read_csv(DATA_PROCESSED / "dim_dates.csv")

# -------------------------
# WRITE TO SQL
# -------------------------
fact_sales.to_sql("fact_sales", conn, if_exists="replace", index=False)
dim_customers.to_sql("dim_customers", conn, if_exists="replace", index=False)
dim_products.to_sql("dim_products", conn, if_exists="replace", index=False)
dim_sellers.to_sql("dim_sellers", conn, if_exists="replace", index=False)
dim_dates.to_sql("dim_dates", conn, if_exists="replace", index=False)

print("🎯 All tables loaded into SQLite")

conn.close()
print("✅ Database connection closed")
