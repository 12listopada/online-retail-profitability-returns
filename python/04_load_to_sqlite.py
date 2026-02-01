"""
Loads processed datasets into a SQLite database.

- Creates analytical tables in SQLite
- Inserts enriched order-item data
- Prepares the database as a reporting layer for Power BI
"""

# 04_load_to_sqlite.py
import sqlite3
import pandas as pd

DB = "retail.db"

def main():
    orders = pd.read_csv("orders_enriched.csv", parse_dates=["order_date", "shipped_date"])
    items = pd.read_csv("order_items_enriched.csv", parse_dates=["order_date", "shipped_date"])
    cost = pd.read_csv("product_cost_history.csv", parse_dates=["month_start"])

    con = sqlite3.connect(DB)

    orders.to_sql("orders", con, if_exists="replace", index=False)
    items.to_sql("order_items", con, if_exists="replace", index=False)
    cost.to_sql("product_cost_history", con, if_exists="replace", index=False)

    # indexes
    cur = con.cursor()
    cur.executescript("""
    CREATE INDEX IF NOT EXISTS idx_items_order_id ON order_items(order_id);
    CREATE INDEX IF NOT EXISTS idx_items_country ON order_items(shipping_country);
    CREATE INDEX IF NOT EXISTS idx_items_shipdate ON order_items(shipped_date);
    CREATE INDEX IF NOT EXISTS idx_items_product ON order_items(product_id);
    """)
    con.commit()

    print("orders rows:", len(orders))
    print("order_items rows:", len(items))
    print("product_cost_history rows:", len(cost))
    print(f"Saved DB: {DB}")

if __name__ == "__main__":
    main()
