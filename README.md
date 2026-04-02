# RFM Customer Segmentation Analysis
### Python · Pandas · Plotly

A end-to-end customer segmentation analysis built for e-commerce and DTC brands. 
Uses RFM (Recency, Frequency, Monetary) scoring to identify high-value customers, flag churn risk, and surface actionable retention insights.

---

## Business Context

Not all customers are equal, but some brands treat them like they are.

This analysis segments a retail customer base into behavioral tiers using RFM methodology, answering questions like:
- Who are the VIP customers, and what does their purchase behavior actually look like?
- Which customers are slipping toward churn before it shows up in revenue?
- Where should retention budget be concentrated for maximum ROI?

---

## Dataset

**coastal_retail.csv** — a synthetic transactional dataset modelled after a coastal lifestyle brand. 

| Field | Description |
|-------|-------------|
| `InvoiceNo` | Unique transaction ID (prefix `C` = return) |
| `StockCode` | Product SKU |
| `Description` | Product name |
| `Quantity` | Units purchased (negative for returns) |
| `InvoiceDate` | Transaction timestamp |
| `UnitPrice` | Price per unit |
| `CustomerID` | Unique customer identifier |
| `Country` | Customer location |

~11,600 rows · 1,200 customers 

---

## Methodology

### 1. RFM Score Calculation
Each customer is scored 1–4 on three dimensions using quartile-based binning:

| Dimension | Definition | Scoring logic |
|-----------|-----------|---------------|
| **Recency** | Days since last purchase | Lower = better (inverted scale) |
| **Frequency** | Number of transactions | Higher = better |
| **Monetary** | Total revenue generated | Higher = better |

### 2. Segment Assignment
Composite RFM scores (max 12) map to six customer segments:

| Segment | Score Range | Strategic Priority |
|---------|-------------|-------------------|
| VIP | 10–12 | Reward & retain |
| Loyal | 9 | Upsell & cross-sell |
| Potential Loyal | 7–8 | Nurture to loyalty |
| At Risk | 5–6 | Re-engagement campaigns |
| Can't Lose | 4 | Win-back urgency |
| Lost | 3 | Low-cost reactivation or sunset |

### 3. VIP Deep Dive
Focused analysis on the highest-value segment including:
- Distribution of R/F/M values via box plots
- Correlation heatmap to identify which dimensions drive VIP status

---

## Visualizations

| Chart | Insight |
|-------|---------|
| Segment distribution bar chart | How the customer base splits across value tiers |
| VIP box plots | Spread and outliers in VIP recency, frequency, spend |
| Correlation heatmap | Relationship between R, F, M within the VIP segment |
| Grouped bar — avg R/F/M by segment | How each segment scores across all three dimensions |

---

## Key Findings

- **VIP customers** represent 28% of the base but drive a disproportionate share of revenue 
- **At Risk** segemnt shows high monetary scores with declining recency, indicating lapsed high-spenders worth targeting with win-back flows. 
- **Frequency and Monetary** show a near-perfect correlation (0.95) within the VIP segment, confirming that VIP status is driven by purchase frequency rather than basket size. Recency shows weak correlation with both other dimensions (−0.14), suggesting that even the most valuable customers don't necessarily shop on a rigid schedule. It means that retention tactics for VIPs should prioritise purchase frequency triggers suc as replenishment reminders, early access drops, and loyalty perks over upselling higher-priced items.

---

## How to Run
```bash
pip install pandas plotly
python rfm_analysis.py
```

---

## Skills Demonstrated

`pandas` · `plotly.express` · `plotly.graph_objects` · quantile-based scoring · customer segmentation · cohort logic · data visualization · e-commerce analytics

---

## About

Built as part of a portfolio focused on growth analytics for DTC and e-commerce brands. 
I'm a freelance e-commerce consultant specialising in retention strategy, customer analytics, and performance reporting for fashion and lifestyle brands.
