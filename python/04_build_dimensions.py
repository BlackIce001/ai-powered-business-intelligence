import pandas as pd
from pathlib import Path

# -------------------------
# PROJECT PATHS
# -------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"

# -------------------------
# LOAD CLEANED DATA
# -------------------------
customers = pd.read_csv(DATA_PROCESSED / "customers_clean_ml.csv")
products = pd.read_csv(DATA_PROCESSED / "products_clean_ml.csv")
orders = pd.read_csv(DATA_PROCESSED / "orders_clean_ml.csv")
order_items = pd.read_csv(DATA_PROCESSED / "order_items_clean_ml.csv")

print("✅ Cleaned data loaded for dimensions")

# -------------------------
# DIM_CUSTOMERS
# -------------------------
dim_customers = customers[[
    "customer_id",
    "customer_unique_id",
    "customer_city",
    "customer_state"
]].drop_duplicates().reset_index(drop=True)

dim_customers["customer_key"] = dim_customers.index + 1

# -------------------------
# DIM_PRODUCTS
# -------------------------
dim_products = products[[
    "product_id",
    "product_category_name_english",
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm"
]].drop_duplicates().reset_index(drop=True)

dim_products["product_key"] = dim_products.index + 1

# -------------------------
# DIM_SELLERS
# -------------------------
dim_sellers = order_items[[
    "seller_id"
]].drop_duplicates().reset_index(drop=True)

dim_sellers["seller_key"] = dim_sellers.index + 1

# -------------------------
# DIM_DATES
# -------------------------
dim_dates = orders[[
    "order_purchase_timestamp"
]].drop_duplicates()

dim_dates["order_date"] = pd.to_datetime(
    dim_dates["order_purchase_timestamp"]
)

dim_dates["date_key"] = dim_dates["order_date"].dt.strftime("%Y%m%d").astype(int)
dim_dates["year"] = dim_dates["order_date"].dt.year
dim_dates["month"] = dim_dates["order_date"].dt.month
dim_dates["day"] = dim_dates["order_date"].dt.day
dim_dates["weekday"] = dim_dates["order_date"].dt.day_name()

dim_dates = dim_dates[[
    "date_key",
    "order_date",
    "year",
    "month",
    "day",
    "weekday"
]].reset_index(drop=True)

# -------------------------
# SAVE DIMENSIONS
# -------------------------
dim_customers.to_csv(DATA_PROCESSED / "dim_customers.csv", index=False)
dim_products.to_csv(DATA_PROCESSED / "dim_products.csv", index=False)
dim_sellers.to_csv(DATA_PROCESSED / "dim_sellers.csv", index=False)
dim_dates.to_csv(DATA_PROCESSED / "dim_dates.csv", index=False)

print("🎯 DIMENSION TABLES CREATED")
print("Customers:", dim_customers.shape)
print("Products:", dim_products.shape)
print("Sellers:", dim_sellers.shape)
print("Dates:", dim_dates.shape)
