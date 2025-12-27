import pandas as pd
import numpy as np
from pathlib import Path

from sklearn.impute import KNNImputer
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# -------------------------
# PROJECT PATH SETUP
# -------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"

# -------------------------
# LOAD RAW DATA
# -------------------------
customers = pd.read_csv(DATA_RAW / "olist_customers_dataset.csv")
orders = pd.read_csv(DATA_RAW / "olist_orders_dataset.csv")
order_items = pd.read_csv(DATA_RAW / "olist_order_items_dataset.csv")
payments = pd.read_csv(DATA_RAW / "olist_order_payments_dataset.csv")
products = pd.read_csv(DATA_RAW / "olist_products_dataset.csv")
category_translation = pd.read_csv(
    DATA_RAW / "product_category_name_translation.csv"
)

print("✅ Raw data loaded")

# -------------------------
# RULE-BASED CLEANING
# -------------------------
customers = customers.drop_duplicates()
orders = orders.drop_duplicates()
order_items = order_items.drop_duplicates()

date_cols = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for col in date_cols:
    orders[col] = pd.to_datetime(orders[col], errors="coerce")

order_items["revenue"] = (
    order_items["price"] + order_items["freight_value"]
)

# -------------------------
# ML STEP 1: KNN IMPUTATION
# -------------------------
orders["delivery_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_purchase_timestamp"]
).dt.days

imputer = KNNImputer(n_neighbors=5)
orders[["delivery_days"]] = imputer.fit_transform(
    orders[["delivery_days"]]
)

print("✅ Missing values handled with KNN Imputer")

# -------------------------
# ML STEP 2: OUTLIER DETECTION
# -------------------------
numeric_features = order_items[
    ["price", "freight_value", "revenue"]
]

scaler = StandardScaler()
scaled_data = scaler.fit_transform(numeric_features)

iso_forest = IsolationForest(
    n_estimators=100,
    contamination=0.02,
    random_state=42
)

order_items["outlier"] = iso_forest.fit_predict(scaled_data)
order_items = order_items[order_items["outlier"] == 1]
order_items = order_items.drop(columns=["outlier"])

print("✅ Outliers removed using Isolation Forest")

# -------------------------
# DATA ENRICHMENT
# -------------------------
products = products.merge(
    category_translation,
    on="product_category_name",
    how="left"
)

products["product_category_name_english"] = (
    products["product_category_name_english"]
    .fillna("unknown")
)

# -------------------------
# SAVE CLEAN DATA
# -------------------------
customers.to_csv(
    DATA_PROCESSED / "customers_clean_ml.csv", index=False
)
orders.to_csv(
    DATA_PROCESSED / "orders_clean_ml.csv", index=False
)
order_items.to_csv(
    DATA_PROCESSED / "order_items_clean_ml.csv", index=False
)
payments.to_csv(
    DATA_PROCESSED / "payments_clean_ml.csv", index=False
)
products.to_csv(
    DATA_PROCESSED / "products_clean_ml.csv", index=False
)

print("🎯 ML-based data cleaning completed successfully")
