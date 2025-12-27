import sqlite3
import pandas as pd
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "data" / "mindone_dw.db"
OUT_DIR = PROJECT_ROOT / "data" / "powerbi"

OUT_DIR.mkdir(exist_ok=True)

conn = sqlite3.connect(DB_PATH)

tables = [
    "fact_sales",
    "dim_customers",
    "dim_products"
]

for table in tables:
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    df.to_csv(OUT_DIR / f"{table}.csv", index=False)
    print(f"Exported {table}")

conn.close()
print("✅ All tables exported for Power BI")
