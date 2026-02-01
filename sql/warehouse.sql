-- sql/warehouse.sql

DROP TABLE IF EXISTS fact_order_item_profit;

CREATE TABLE fact_order_item_profit AS
SELECT
  oi.order_item_id,
  oi.order_id,
  oi.customer_id,
  oi.product_id,
  oi.product_description,
  oi.quantity,
  oi.unit_price,
  oi.line_discount_amount,
  oi.order_date,
  oi.shipped_date,
  oi.shipping_country,
  oi.channel,

  -- profitability components
  oi.gross_item_revenue,
  oi.net_item_revenue,
  oi.unit_cost,
  oi.item_cogs,
  oi.allocated_shipping_cost_item,
  oi.is_return,
  oi.transaction_type,
  oi.return_amount,
  oi.contribution_margin

FROM order_items oi;

-- Helpful indexes
CREATE INDEX IF NOT EXISTS idx_fact_country ON fact_order_item_profit(shipping_country);
CREATE INDEX IF NOT EXISTS idx_fact_shipdate ON fact_order_item_profit(shipped_date);
CREATE INDEX IF NOT EXISTS idx_fact_order ON fact_order_item_profit(order_id);

-- =========================================================
-- CHECKS / VALIDATION VIEWS
-- =========================================================

DROP VIEW IF EXISTS vw_country_profitability;
CREATE VIEW vw_country_profitability AS
SELECT
  shipping_country,
  ROUND(SUM(net_item_revenue),2) AS net_revenue,
  ROUND(SUM(contribution_margin),2) AS contribution_margin,
  ROUND(1.0 * SUM(contribution_margin) / NULLIF(SUM(net_item_revenue),0), 4) AS contribution_margin_pct,
  ROUND(1.0 * SUM(ABS(line_discount_amount)) / NULLIF(SUM(gross_item_revenue),0), 4) AS discount_pct_gross,
  ROUND(1.0 * SUM(allocated_shipping_cost_item) / NULLIF(SUM(net_item_revenue),0), 4) AS shipping_pct_net,
  ROUND(1.0 * SUM(return_amount) / NULLIF(SUM(net_item_revenue),0), 4) AS return_impact_pct
FROM fact_order_item_profit
GROUP BY shipping_country;

DROP VIEW IF EXISTS vw_monthly_trends;
CREATE VIEW vw_monthly_trends AS
SELECT
  substr(shipped_date, 1, 7) AS shipped_month,
  ROUND(SUM(net_item_revenue),2) AS net_revenue,
  ROUND(SUM(contribution_margin),2) AS contribution_margin,
  ROUND(1.0 * SUM(contribution_margin) / NULLIF(SUM(net_item_revenue),0), 4) AS contribution_margin_pct
FROM fact_order_item_profit
GROUP BY substr(shipped_date, 1, 7)
ORDER BY shipped_month;

-- quick data sanity checks
-- 1) how many return lines
-- SELECT SUM(is_return) AS return_lines FROM fact_order_item_profit;

-- 2) orders with net revenue <= 0
-- SELECT COUNT(DISTINCT order_id) FROM fact_order_item_profit
-- GROUP BY order_id HAVING SUM(net_item_revenue) <= 0;

-- 3) biggest profit destroyers
-- SELECT * FROM vw_country_profitability ORDER BY contribution_margin_pct ASC LIMIT 15;
