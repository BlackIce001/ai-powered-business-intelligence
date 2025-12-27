import sqlite3
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "data" / "mindone_dw.db"

conn = sqlite3.connect(DB_PATH)

# 1️⃣ Total Revenue
q1 = """
SELECT ROUND(SUM(revenue), 2) AS total_revenue
FROM fact_sales;
"""
print("Total Revenue:")
print(pd.read_sql(q1, conn), "\n")

# 2️⃣ Revenue by Month
q2 = """
SELECT d.year, d.month, ROUND(SUM(f.revenue), 2) AS monthly_revenue
FROM fact_sales f
JOIN dim_dates d ON d.order_date = f.order_date
GROUP BY d.year, d.month
ORDER BY d.year, d.month;
"""
print("Revenue by Month:")
print(pd.read_sql(q2, conn), "\n")

# 3️⃣ Top 10 Products by Revenue
q3 = """
SELECT p.product_category_name_english, ROUND(SUM(f.revenue), 2) AS revenue
FROM fact_sales f
JOIN dim_products p ON p.product_id = f.product_id
GROUP BY p.product_category_name_english
ORDER BY revenue DESC
LIMIT 10;
"""
print("Top 10 Product Categories:")
print(pd.read_sql(q3, conn), "\n")

# 4️⃣ Average Delivery Time
q4 = """
SELECT ROUND(AVG(delivery_days), 2) AS avg_delivery_days
FROM fact_sales;
"""
print("Average Delivery Time:")
print(pd.read_sql(q4, conn))

conn.close()
