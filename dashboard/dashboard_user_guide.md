# Military Base Supply Control Dashboard – Documentation

A dashboard for visualizing key operational and supply chain metrics for **Supplies** across military bases, vendors, and supply categories.

**Timeline Note:** The dataset simulates operational activity over approximately 90 days. All metrics reflect this short-term window unless otherwise stated.

## Dashboard Visuals Overview

| **Category**               | **Visualization Title**                          | **Metric**                                  | **Description**                                                                                          |
|----------------------------|--------------------------------------------------|---------------------------------------------|----------------------------------------------------------------------------------------------------------|
| Vendor Delivery Metrics | **On-Time Delivery Rate by Vendor**              | `% of deliveries with delay_days <= 0`      | Measures delivery punctuality for each vendor. High % reflects vendor reliability. Sorted descending.    |
| Vendor Delivery Metrics | **Average Delivery Delay (Days) by Vendor**      | `Average of delay_days`                     | Shows the mean delay per vendor across all deliveries. Lower is better.                                 |
| Vendor Delivery Metrics | **% of Deliveries Delayed Over 2 Days**          | `% of deliveries where delay_days > 2`      | Flags vendors consistently failing timely delivery expectations. Helps assess SLA risk.                 |
| Vendor Delivery Metrics | **Vendor Reliance Heatmap**                      | `Order volume by base and vendor`           | Density heatmap showing order distribution to identify single-vendor dependencies by base.              |
| Inventory Risk          | **Inventory Risk (Coverage < 35 Days)**          | `days_remaining < 35`                       | Scatter plot showing which bases and categories are low on stock. Point size indicates volume at risk.  |
| Inventory Risk          | **Critical Base-Category Inventory (<35 Days)**  | `days_remaining < 35, sorted by urgency`    | Bar chart of specific base-category combinations requiring immediate attention.                          |
| Inventory Management    | **Aging Inventory Risk by Supply Category**      | `Days since last inventory update`          | Shows recency of inventory checks. High values may indicate outdated stock or risk of spoilage.         |
| Financial Performance   | **Budget Utilization (%)**                       | `budget_spent / budget_allocated`           | Heatmap of actual vs. planned spending. Useful for spotting over/under-spending trends.                |
| Financial Performance   | **Cost Breakdown by Base and Supply Category**   | `budget_spent by base and category`         | Stacked bar chart showing spending distribution across supply categories by base.                       |
| Route Security          | **Average Route Risk Score by Base**             | `Avg route_risk_level (Low=1 to High=3)`    | Quantifies how often high-risk transport routes are used per base. High values indicate supply risk.    |
| Procurement Efficiency  | **Procurement Lead Time by Supply Category**     | `actual_delivery_date - order_date`         | Box plot of time between ordering and delivery. Outliers reveal inefficiencies or chokepoints.          |
| Emergency Orders        | **Emergency Order Rate by Base**                 | `% of orders marked as 'Emergency'`         | Highlights bases frequently relying on emergency procurement, often indicating poor planning.           |
| Composite Risk          | **Composite Base Risk Index**                    | `Avg of: route_risk, low supply, overspend, emergency freq` | Summarizes all critical risk drivers into a unified risk score (0-100). Helps prioritize attention.  |

## Datasets Referenced

| Dataset                    | Description                                                                 |
|----------------------------|-----------------------------------------------------------------------------|
| `supply_deliveries.csv`       | Delivery records including vendor, base, route risk, actual vs expected dates |
| `supply_orders.csv`           | Order logs including priority (Emergency/Urgent/Routine), quantities, and dates |
| `base_inventory_supply.csv`   | Current inventory levels, average consumption, days remaining                |
| `supply_budget.csv`           | Budget allocation vs. actual spend, by base and supply category             |

## Interpretation Notes

**High Route Risk + High Emergency Rate**  
→ Indicates bases vulnerable to logistical disruptions and unplanned spending.

**Low Days Remaining + High Avg Delay**  
→ Base may run out of supply before vendor can fulfill resupply, signaling a readiness issue.

**High Aging Inventory + Low Emergency Rate**  
→ Suggests possible stockpiling or data not refreshed — requires auditing.

## Dashboard Usage Scenarios

**Weekly Operational Briefs**  
Flag bases requiring resupply or budget reallocation.

**Vendor SLA Reviews**  
Identify performance bottlenecks and negotiate accountability.

**Strategic Planning**  
Allocate convoy or airlift support based on route risk data.

**Audit & Compliance**  
Use budget and aging indicators to detect policy non-compliance.