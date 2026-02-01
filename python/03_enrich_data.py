"""
Enriches transactional data with business and financial metrics.

- Calculates gross and net item revenue
- Applies discounts and return logic
- Prepares profitability-related fields for analysis
"""

# 03_enrich_data.py
import pandas as pd
import numpy as np

ORDERS_CSV = "orders.csv"
ITEMS_CSV = "order_items.csv"

ORDERS_OUT = "orders_enriched.csv"
ITEMS_OUT = "order_items_enriched.csv"
COST_OUT = "product_cost_history.csv"

def main():
    orders = pd.read_csv(ORDERS_CSV, parse_dates=["order_date", "shipped_date"])
    items = pd.read_csv(ITEMS_CSV, parse_dates=["order_date", "shipped_date"])

    # --- returns flag (based on quantity < 0)
    items["is_return"] = (items["quantity"] < 0).astype("int64")
    items["transaction_type"] = np.where(items["is_return"] == 1, "return", "sale")

    # --- revenue (gross/net)
    items["gross_item_revenue"] = items["quantity"] * items["unit_price"]
    # net item revenue includes discount amount (discount is negative)
    items["net_item_revenue"] = items["gross_item_revenue"] + items["line_discount_amount"]

    # --- create product cost history (monthly costs)
    # simulate cost as 55%–85% of unit price baseline
    prod_base = (
        items.groupby("product_id", as_index=False)
        .agg(avg_price=("unit_price", "mean"))
    )
    prod_base["base_cost"] = prod_base["avg_price"] * np.random.uniform(0.55, 0.85, len(prod_base))

    # cost per month (simple 3-step variation)
    months = pd.date_range(items["shipped_date"].min().normalize(), items["shipped_date"].max().normalize(), freq="MS")
    cost_rows = []
    for _, r in prod_base.iterrows():
        for m in months:
            drift = np.random.uniform(-0.03, 0.03)
            cost_rows.append([r["product_id"], m, max(0.01, r["base_cost"] * (1.0 + drift)), "simulated"])
    cost_hist = pd.DataFrame(cost_rows, columns=["product_id", "month_start", "unit_cost", "source"])
    cost_hist.to_csv(COST_OUT, index=False)

    # attach unit cost by shipped month
    items["month_start"] = items["shipped_date"].dt.to_period("M").dt.to_timestamp()
    items = items.merge(
        cost_hist[["product_id", "month_start", "unit_cost"]],
        on=["product_id", "month_start"],
        how="left"
    )
    items["unit_cost"] = items["unit_cost"].fillna(items["unit_price"] * 0.7)

    # item COGS (keep sign with quantity, so returns reverse COGS)
    items["item_cogs"] = items["quantity"] * items["unit_cost"]

    # --- shipping cost allocation (per order -> allocate to items by abs(net revenue))
    # simulate shipping by country baseline
    country_base = orders[["shipping_country"]].drop_duplicates().copy()
    country_base["ship_rate"] = np.where(country_base["shipping_country"].isin(["Norway", "Denmark"]), 
                                         np.random.uniform(0.05, 0.12, len(country_base)),
                                         np.random.uniform(0.01, 0.04, len(country_base)))
    orders = orders.merge(country_base, on="shipping_country", how="left")

    # order net revenue (sum of item net revenue)
    order_net = items.groupby("order_id", as_index=False).agg(order_net=("net_item_revenue", "sum"))
    orders = orders.merge(order_net, on="order_id", how="left")

    # shipping cost per order = max(0, rate * positive net revenue)
    orders["shipping_cost_order"] = (orders["ship_rate"] * orders["order_net"].clip(lower=0)).fillna(0.0)

    # allocate shipping to items
    items = items.merge(orders[["order_id", "shipping_cost_order"]], on="order_id", how="left")
    alloc_base = items["net_item_revenue"].abs()
    alloc_sum = items.groupby("order_id")["net_item_revenue"].transform(lambda s: s.abs().sum()).replace(0, np.nan)
    items["allocated_shipping_cost_item"] = (items["shipping_cost_order"] * (alloc_base / alloc_sum)).fillna(0.0)

    # return_amount (impact measure) — net revenue on return lines (stored as positive impact)
    items["return_amount"] = np.where(items["is_return"] == 1, items["net_item_revenue"].abs(), 0.0)

    # contribution margin (simple: net revenue - cogs - allocated shipping)
    # NOTE: discounts already included in net_item_revenue
    items["contribution_margin"] = items["net_item_revenue"] - items["item_cogs"] - items["allocated_shipping_cost_item"]

    # clean export
    orders.to_csv(ORDERS_OUT, index=False)
    items.drop(columns=["month_start"], errors="ignore").to_csv(ITEMS_OUT, index=False)

    print(f"Saved: {ORDERS_OUT}, {ITEMS_OUT}, {COST_OUT}")
    print("orders_enriched shape:", orders.shape)
    print("order_items_enriched shape:", items.shape)
    print("cost_history shape:", cost_hist.shape)
    print("Return lines:", int(items["is_return"].sum()))
    print("Discounted lines:", int((items["line_discount_amount"] != 0).sum()))

if __name__ == "__main__":
    main()
