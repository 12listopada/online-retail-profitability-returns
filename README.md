# Online Retail: Return Impact & Profitability Analysis  
**SQL • Python • Power BI**

End-to-end analytics project simulating a real business workflow:  
**raw Excel → Python cleaning & enrichment → SQLite (warehouse layer) → SQL validation → Power BI semantic model & dashboard → business insights & recommendations**

---

## 1) Project Objective

The goal of this project was to build a **portfolio-ready business analytics solution** that mirrors real-world data workflows.

Key objectives:
- create a clean analytical dataset at **order-item (line) level**
- measure profitability using **gross margin** and **contribution margin**
- quantify the financial impact of **returns**, **discounts**, and **shipping costs**
- identify profitability drivers across markets and over time
- deliver an executive-ready **Power BI report** with clear insights and recommendations

---

## 2) Business Questions

This analysis focuses on answering the following business questions:

1. Which countries generate the highest revenue and profitability?
2. Which markets have the highest **return impact**, and how does it affect contribution margin?
3. Are high return rates driven by aggressive discounting?
4. How significant are shipping costs across markets (as % of revenue)?
5. Where does profitability erode over time and what are the key drivers?
6. Is Norway an outlier — and if so, is the issue **pricing-related or operational**?

---

## 3) Dataset

- Source: Online Retail transactional dataset (Excel)
- Scale: ~600k+ rows
- Grain: **order-item (line) level**

> Raw data is not included in this repository.

---

## 4) Project Structure

├── data
│ ├── raw
│ └── processed
├── python
│ ├── 01_load_and_export.py
│ ├── 02_build_orders_items.py
│ ├── 03_enrich_data.py
│ ├── 04_load_to_sqlite.py
│ └── 05_run_sql.py
├── sql
│ └── warehouse.sql
├── powerbi
│ └── README.md
├── docs
│ └── Retail_Return_Impact_Report.pdf
└── README.md

---

## 5) Data Processing & Modeling

### Python (data processing & enrichment)

Python (pandas) was used to:
- efficiently load a large Excel dataset
- clean and standardize columns (dates, numeric fields, IDs)
- split raw data into logical entities (orders, order items)
- enrich data with calculated fields:
  - gross item revenue
  - net item revenue
  - discount amount and discount %
  - allocated shipping cost per item
  - return flags and return impact
- export intermediate CSV files for validation
- ensure correct signs and data types (e.g. negative quantities for returns)

---

### SQLite & SQL (warehouse and validation)

- processed data loaded into **SQLite (`retail.db`)**
- designed a fact table at line level:  
  **`fact_order_item_profit`**
- SQL used for:
  - aggregation checks
  - reconciliation of revenue, margin, and return metrics
  - validation before Power BI ingestion

---

### Power BI (semantic model & dashboard)

- star-schema–like model with a dedicated **Date table**
- DAX measures for:
  - Net Revenue
  - Gross Margin / Gross Margin %
  - Contribution Margin / Contribution Margin %
  - Return Impact %
  - Discount % of Revenue
  - Shipping Cost % of Net Item Revenue
  - % Orders with Negative Contribution
  - Return Lines

Report pages:
1. **Executive Overview** – KPIs, trends, profitability by country
2. **Profitability Drivers** – returns vs discounts vs shipping
3. **Returns Deep Dive (Norway)** – time trends, seasonality, multivariate analysis

---

## 6) Key Insights

- Norway is a clear outlier with **extreme return impact**, exceeding 100% of net item revenue.
- Most markets cluster within a narrow discount–return range, indicating a **weak relationship between discounting and returns**.
- Returns are the most damaging profitability driver compared to discounts and shipping costs in selected markets.
- Return volumes show seasonal patterns, with peaks in late-year months.

---

## 7) Business Recommendations

1. Investigate operational drivers behind Norway’s return behavior (logistics, fulfillment quality, delivery lead times).
2. Apply stricter return controls in markets with high return impact.
3. Review shipping contracts and pricing in markets with elevated shipping cost ratios.
4. Reduce discounting where it does not improve profitability or customer behavior.

---

## 8) Deliverables

- **Power BI report (PDF):**  
  `docs/Retail_Return_Impact_Report.pdf`

---

## 9) Future Improvements

If additional data were available:
- analyze returns by product category and return reason
- include carrier / warehouse data to identify operational bottlenecks
- segment customers (new vs returning) and evaluate return behavior
- build a simple predictive model to flag high-risk orders

---

## 10) Tools & Technologies

- **Python (pandas)** – data cleaning & enrichment  
- **SQLite + SQL** – analytical storage & validation  
- **Power BI + DAX** – modeling, metrics, and visualization
