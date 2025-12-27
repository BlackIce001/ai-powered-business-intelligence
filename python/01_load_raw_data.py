import pandas as pd
from pathlib import Path

# -------------------------
# PROJECT PATH SETUP
# -------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = PROJECT_ROOT / "data" / "raw"

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

print("Customers:", customers.shape)
print("Orders:", orders.shape)
print("Order Items:", order_items.shape)
print("Payments:", payments.shape)
print("Products:", products.shape)
print("Category Translation:", category_translation.shape)

print("\nOrders Preview:")
print(orders.head())
