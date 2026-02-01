# 05_run_sql.py
import sqlite3

DB = "retail.db"
SQL_FILE = "sql/warehouse.sql"

def main():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    with open(SQL_FILE, "r", encoding="utf-8") as f:
        sql = f.read()

    cur.executescript(sql)
    con.commit()

    # checks
    n = cur.execute("SELECT COUNT(*) FROM fact_order_item_profit;").fetchone()[0]
    print("fact_order_item_profit rows:", n)

    totals = cur.execute("""
        SELECT
          ROUND(SUM(net_item_revenue),2) AS net_rev,
          ROUND(SUM(gross_item_revenue),2) AS gross_rev,
          ROUND(SUM(item_cogs),2) AS cogs,
          ROUND(SUM(allocated_shipping_cost_item),2) AS ship,
          ROUND(SUM(contribution_margin),2) AS cm
        FROM fact_order_item_profit;
    """).fetchone()
    print("Totals:", totals)

    con.close()

if __name__ == "__main__":
    main()
