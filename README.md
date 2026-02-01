# Online Retail: Return Impact & Profitability Analysis (SQL • Python • Power BI)

End-to-end analytics project: **raw Excel → Python cleaning/enrichment → SQLite (warehouse layer) → SQL validation → Power BI semantic model & dashboard → business insights & recommendations**.

---

## 1) Project Goals (Main Intent)

Build a portfolio-quality analytics workflow that simulates a real business environment:
- create a clean analytical dataset at **order-item (line) level**
- quantify profitability using **gross margin** and **contribution margin**
- measure the financial impact of **returns**, **discounts**, and **shipping costs**
- deliver an executive-ready **Power BI report** with clear drivers, trends, and a focused deep dive

---

## 2) Business Questions

1. Which markets (countries) drive the highest revenue and profitability?
2. Which markets have the highest **return impact** and how does it affect contribution margin?
3. Are high returns correlated with aggressive discounting?
4. How large is the shipping cost burden across markets (as % of revenue)?
5. Where do we see margin erosion over time and what are the key drivers?
6. Is Norway an outlier and if so, **what explains it** (pricing vs operations)?

---

## 3) Dataset

- Source: Online Retail transactional dataset (Excel)
- Scale: ~600k+ rows
- Grain (analysis level): **order-item (line)**

> Note: Raw data is not included in this repository.

---

## 4) Workflow / Pipeline

### Python (data processing & transformation)
Used Python (pandas) to:
- load large Excel efficiently
- clean & standardize columns (dates, numeric fields, IDs)
- split raw data into logical entities (orders, order items)
- enrich data with calculated fields:
  - gross item revenue, net item revenue
  - discount amounts / discount %
  - allocated shipping cost per item
  - return flags and return impact
- export intermediate CSVs to validate transformations step-by-step
- ensure correct signs and types (e.g., negative quantities for returns)

### SQLite (warehouse layer) + SQL validation
- loaded processed data into **retail.db**
- designed a fact table at line level: **fact_order_item_profit**
- used SQL for:
  - row count and aggregation checks
  - metric sanity validation prior to Power BI

### Power BI (semantic model + dashboard)
- clean data model with a dedicated **Date table**
- DAX measures for:
  - Net Revenue, Gross Margin, Contribution Margin
  - Return Impact %, Discount %, Shipping Cost %
  - % Orders with Negative Contribution
- report pages:
  1. **Executive Overview** – KPIs and trends + profitability by country
  2. **Profitability Drivers** – returns vs discounts vs shipping by country
  3. **Returns Deep Dive – Norway** – trends, seasonality, and multivariate view

---

## 5) Key Metrics (DAX)

Core metrics used in the report:
- Net Revenue
- Gross Margin / Gross Margin %
- Contribution Margin / Contribution Margin %
- Return Impact %
- Discount % of Revenue
- Shipping Cost % of Net Item Revenue
- % Orders with Negative Contribution
- Return Lines

---

## 6) Key Insights

- Norway is a clear outlier with extremely high return impact (over 100% of net item revenue).
- Most markets cluster within a narrow discount–return range, suggesting **weak correlation** between discounting and returns.
- Returns are the most “painful” profitability driver compared to discounts and shipping in selected markets.
- Return volumes show seasonal patterns (peaks in late-year months), useful for operational planning.

---

## 7) Recommendations

1. Investigate operational drivers behind Norway’s returns (logistics, delivery lead times, fulfillment quality).
2. Introduce stricter return policy controls in high-impact markets (where feasible).
3. Review shipping pricing strategy or carrier contracts for markets with high shipping % of revenue.
4. Reduce unnecessary discounting in markets where it does not improve return behavior or margin.

---

## 8) Report Output

- PDF export: see `report/powerbi_report.pdf`
- Screenshots: see `report/screenshots/`

---

## 9) What I would do next (if more data was available)

- analyze returns by product category and return reason
- include carrier / warehouse / fulfillment data to pinpoint operational issues
- segment customers (new vs returning) and evaluate return behavior patterns
- build a simple predictive model to flag high-risk orders (Python)

---

## 10) Tools

- Python (pandas) – processing & enrichment
- SQLite + SQL – storage and validation
- Power BI + DAX – modeling, measures, visualization

## Dashboard Preview

📄 **Power BI Report (PDF)**  
[Download report](docs/Retail_Return_Impact_Report.pdf)
