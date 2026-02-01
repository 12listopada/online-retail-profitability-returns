# 02_build_orders_items.py
import pandas as pd
import numpy as np

RAW_CSV = "online_retail_raw.csv"
ORDERS_CSV = "orders.csv"
ITEMS_CSV = "order_items.csv"

def main():
    df = pd.read_csv(RAW_CSV)

    # Normalize column names from the dataset
    # Expected raw columns: Invoice, StockCode, Description, Quantity, InvoiceDate, Price, Customer ID, Country
    df.rename(columns={
        "Customer ID": "CustomerID",
        "InvoiceDate": "InvoiceDate",
        "StockCode": "StockCode",
        "Description": "Description",
        "Quantity": "Quantity",
        "Price": "UnitPrice",
        "Invoice": "Invoice",
        "Country": "Country"
    }, inplace=True)

    # Parse date
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

    # order_id = invoice
    df["order_id"] = df["Invoice"].astype(str).str.strip()
    df["customer_id"] = df["CustomerID"].fillna(0).astype("int64").astype(str)

    # product fields
    df["product_id"] = df["StockCode"].astype(str).str.strip()
    df["product_description"] = df["Description"].fillna("").astype(str)

    # quantities + price
    df["quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0).astype("int64")
    df["unit_price"] = pd.to_numeric(df["UnitPrice"], errors="coerce").fillna(0.0)

    # order date
    df["order_date"] = df["InvoiceDate"]

    # shipped_date (simple simulation: shipped 1–7 days later for sales, returns keep same shipped_date)
    lag_days = np.random.randint(1, 8, size=len(df))
    df["shipped_date"] = df["order_date"] + pd.to_timedelta(lag_days, unit="D")

    # shipping country
    df["shipping_country"] = df["Country"].fillna("Unknown")

    # channel (simulated)
    channels = np.where(np.random.rand(len(df)) < 0.85, "Online", "Wholesale")
    df["channel"] = channels

    # discount simulation on sales only (returns keep 0 discount line)
    # NOTE: discount stored as negative amount in your model (so ABS() needed later)
    sales_mask = df["quantity"] > 0
    base_line = df["quantity"] * df["unit_price"]
    disc_rate = np.where(np.random.rand(len(df)) < 0.35, np.random.uniform(0.02, 0.35, len(df)), 0.0)
    df["line_discount_amount"] = np.where(sales_mask, -1.0 * base_line * disc_rate, 0.0)

    # Build orders table (one row per order_id)
    orders = (
        df.groupby("order_id", as_index=False)
          .agg(
              customer_id=("customer_id", "first"),
              order_date=("order_date", "min"),
              shipped_date=("shipped_date", "max"),
              shipping_country=("shipping_country", "first"),
              channel=("channel", "first"),
              order_line_count=("order_id", "size"),
          )
    )

    # Build order_items table
    df = df.reset_index(drop=True)
    df["order_item_id"] = (df.index + 1).astype("int64")

    items = df[[
        "order_item_id",
        "order_id",
        "customer_id",
        "product_id",
        "product_description",
        "quantity",
        "unit_price",
        "line_discount_amount",
        "order_date",
        "shipped_date",
        "shipping_country",
        "channel",
    ]].copy()

    orders.to_csv(ORDERS_CSV, index=False)
    items.to_csv(ITEMS_CSV, index=False)

    print(f"Saved: {ORDERS_CSV}, {ITEMS_CSV}")
    print("orders shape:", orders.shape)
    print("order_items shape:", items.shape)
    print("order_items columns:", list(items.columns))

if __name__ == "__main__":
    main()
