import pandas as pd
from pathlib import Path

# -------------------------
# PROJECT PATHS
# -------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"

# -------------------------
# LOAD CLEANED DATA (ML CLEANED)
# -------------------------
customers = pd.read_csv(DATA_PROCESSED / "customers_clean_ml.csv")
orders = pd.read_csv(DATA_PROCESSED / "orders_clean_ml.csv")
order_items = pd.read_csv(DATA_PROCESSED / "order_items_clean_ml.csv")
payments = pd.read_csv(DATA_PROCESSED / "payments_clean_ml.csv")
products = pd.read_csv(DATA_PROCESSED / "products_clean_ml.csv")

print("✅ Cleaned data loaded")

# -------------------------
# PREPARE ORDERS
# -------------------------
orders_fact = orders[[
    "order_id",
    "customer_id",
    "order_purchase_timestamp",
    "delivery_days"
]].copy()

orders_fact = orders_fact.rename(
    columns={"order_purchase_timestamp": "order_date"}
)


# -------------------------
# AGGREGATE PAYMENTS
# -------------------------
payments_fact = payments.groupby(
    "order_id", as_index=False
)["payment_value"].sum()

# -------------------------
# BUILD FACT TABLE
# -------------------------
fact_sales = (
    order_items
    .merge(orders_fact, on="order_id", how="left")
    .merge(payments_fact, on="order_id", how="left")
)

# -------------------------
# SELECT FINAL FACT COLUMNS
# -------------------------
fact_sales = fact_sales[[
    "order_id",
    "customer_id",
    "product_id",
    "seller_id",
    "order_date",
    "price",
    "freight_value",
    "revenue",
    "payment_value",
    "delivery_days"
]]

# -------------------------
# SAVE FACT TABLE
# -------------------------
fact_sales.to_csv(
    DATA_PROCESSED / "fact_sales.csv",
    index=False
)

print("🎯 FACT TABLE CREATED: fact_sales.csv")
print("Rows:", fact_sales.shape[0])
