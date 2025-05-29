import dash
from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
import numpy as np

# Load datasets
DATA_PATH = "data/dataset"
deliveries = pd.read_csv(os.path.join(DATA_PATH, "supply_deliveries.csv"))
inventory = pd.read_csv(os.path.join(DATA_PATH, "base_inventory_supply.csv"))
budget = pd.read_csv(os.path.join(DATA_PATH, "supply_budget.csv"))
orders = pd.read_csv(os.path.join(DATA_PATH, "supply_orders.csv"))

# Helper mappings
risk_map = {"Low": 1, "Medium": 2, "High": 3}

# Vendor delivery metrics
deliveries["on_time"] = deliveries["delay_days"] <= 0
deliveries["delayed_7"] = deliveries["delay_days"] > 2
vendor_summary = deliveries.groupby("vendor").agg(
    total_deliveries=("order_id", "count"),
    on_time_pct=("on_time", lambda x: round(100 * x.mean(), 2)),
    avg_delay=("delay_days", "mean"),
    delayed_over_7_pct=("delayed_7", lambda x: round(100 * x.mean(), 2))
).reset_index()

vendor_summary = vendor_summary.sort_values("on_time_pct", ascending=False)
fig_vendor = px.bar(vendor_summary, x="vendor", y="on_time_pct", text="on_time_pct",
    title="On-Time Delivery Rate by Vendor", labels={"vendor": "Vendor", "on_time_pct": "% On-Time"})
fig_vendor.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
fig_vendor.update_layout(margin=dict(t=60, b=40), uniformtext_minsize=10)

# Avg delay
avg_delay_fig = px.bar(vendor_summary.sort_values("avg_delay", ascending=False),
    x="vendor", y="avg_delay", text="avg_delay",
    title="Average Delivery Delay (Days) by Vendor",
    labels={"vendor": "Vendor", "avg_delay": "Average Delay (Days)"})
avg_delay_fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
avg_delay_fig.update_layout(margin=dict(t=60, b=40), uniformtext_minsize=10)

# Severe delays
fig_severe = px.bar(vendor_summary.sort_values("delayed_over_7_pct", ascending=False),
    x="vendor", y="delayed_over_7_pct", text="delayed_over_7_pct",
    title="% of Deliveries Delayed Over 2 Days",
    labels={"vendor": "Vendor", "delayed_over_7_pct": "% Delayed > 2 Days"})
fig_severe.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
fig_severe.update_layout(margin=dict(t=60, b=40), uniformtext_minsize=10)

# Inventory coverage
low_inventory = inventory[inventory["days_remaining"] < 35]
fig_inventory = px.scatter(low_inventory, x="base", y="days_remaining", color="supply_category",
    size="inventory_units", title="Inventory Risk (Coverage < 35 Days)",
    labels={"base": "Base", "days_remaining": "Days Remaining", "supply_category": "Supply Category"})
fig_inventory.update_layout(margin=dict(t=60, b=40), uniformtext_minsize=10)

# Budget utilization
budget["utilization"] = (budget["budget_spent"] / budget["budget_allocated"]) * 100
fig_budget = px.density_heatmap(budget, x="base", y="supply_category", z="utilization",
    title="Budget Utilization (%)", color_continuous_scale=px.colors.sequential.Blues,
    labels={"base": "Base", "supply_category": "Supply Category", "utilization": "Utilization (%)"})
fig_budget.update_layout(margin=dict(t=60, b=40), uniformtext_minsize=10)

# Route risk score
deliveries["risk_score"] = deliveries["route_risk_level"].map(risk_map)
route_risk = deliveries.groupby("base")["risk_score"].mean().reset_index()
fig_route_risk = px.bar(route_risk.sort_values("risk_score", ascending=False),
    x="base", y="risk_score", text="risk_score",
    title="Average Route Risk Score by Base", labels={"base": "Base", "risk_score": "Route Risk Score"})
fig_route_risk.update_traces(texttemplate='%{text:.2f}', textposition='outside')
fig_route_risk.update_layout(margin=dict(t=60, b=40), uniformtext_minsize=10)

# Procurement lead time
orders = orders.merge(deliveries[["order_id", "actual_delivery_date"]], on="order_id", how="left")
orders["order_date"] = pd.to_datetime(orders["order_date"])
orders["actual_delivery_date"] = pd.to_datetime(orders["actual_delivery_date"])
orders["lead_time"] = (orders["actual_delivery_date"] - orders["order_date"]).dt.days
fig_lead_time = px.box(orders, x="supply_category", y="lead_time", title="Procurement Lead Time by Supply Category",
    labels={"supply_category": "Supply Category", "lead_time": "Lead Time (Days)"})
fig_lead_time.update_layout(margin=dict(t=60, b=40), uniformtext_minsize=10)

# Emergency procurement
emergency_freq = orders[orders["priority"] == "Emergency"].groupby("base").size() / orders.groupby("base").size()
emergency_df = emergency_freq.reset_index().rename(columns={0: "emergency_rate"})
fig_emergency = px.bar(emergency_df.sort_values("emergency_rate", ascending=False), x="base", y="emergency_rate", text="emergency_rate",
    title="Emergency Order Rate by Base", labels={"base": "Base", "emergency_rate": "% Emergency Orders"})
fig_emergency.update_traces(texttemplate='%{text:.2%}', textposition='outside')
fig_emergency.update_layout(margin=dict(t=60, b=40), uniformtext_minsize=10)

# Aging inventory
inventory["last_updated"] = pd.to_datetime(inventory["last_updated"])
inventory["days_since_update"] = (pd.to_datetime("today") - inventory["last_updated"]).dt.days
fig_aging = px.box(inventory, x="supply_category", y="days_since_update",
    title="Aging Inventory Risk by Supply Category",
    labels={"supply_category": "Supply Category", "days_since_update": "Days Since Last Update"})
fig_aging.update_layout(margin=dict(t=60, b=40), uniformtext_minsize=10)

# Base risk index ---
budget["overspend_flag"] = (budget["budget_spent"] > budget["budget_allocated"] * 1.15).astype(int)
inventory["low_supply_flag"] = (inventory["days_remaining"] < 30).astype(int)
emergency_counts = orders[orders["priority"] == "Emergency"].groupby("base").size()
total_counts = orders.groupby("base").size()
emergency_ratio = (emergency_counts / total_counts).fillna(0)
base_risk = deliveries.groupby("base")["risk_score"].mean().to_frame("route_risk")
base_risk = base_risk.join(
    inventory.groupby("base")["low_supply_flag"].mean().to_frame("low_supply_ratio")
).join(
    budget.groupby("base")["overspend_flag"].mean().to_frame("overspend_ratio")
).join(
    emergency_ratio.to_frame("emergency_ratio")
)
base_risk["base_risk_index"] = base_risk.mean(axis=1) * 100
fig_base_risk = px.bar(base_risk.reset_index().sort_values("base_risk_index", ascending=False), x="base", y="base_risk_index", text="base_risk_index",
    title="Composite Base Risk Index", labels={"base": "Base", "base_risk_index": "Risk Index"})
fig_base_risk.update_traces(texttemplate='%{text:.1f}', textposition='outside')
fig_base_risk.update_layout(margin=dict(t=60, b=40), uniformtext_minsize=10)

# Low inventory table
low_inv_table = low_inventory.sort_values(["days_remaining", "inventory_units"]).reset_index(drop=True)
low_inv_table["label"] = low_inv_table["base"] + " – " + low_inv_table["supply_category"]
fig_low_inv_table = px.bar(low_inv_table, x="label", y="days_remaining",
    title="Critical Base-Category Inventory (<35 Days)",
    labels={"label": "Base – Supply Category", "days_remaining": "Days Remaining"})
fig_low_inv_table.update_traces(texttemplate='%{y}', textposition='outside')
fig_low_inv_table.update_layout(margin=dict(t=60, b=100), uniformtext_minsize=9)

vendor_count = deliveries.groupby(["base", "vendor"]).size().reset_index(name="orders")
fig_vendor_heatmap = px.density_heatmap(
    vendor_count,
    x="base",
    y="vendor",
    z="orders",
    color_continuous_scale=px.colors.sequential.Blues,
    title="Vendor Reliance Heatmap",
    labels={"base": "Base", "vendor": "Vendor", "orders": "Order Volume"}
)
fig_vendor_heatmap.update_layout(margin=dict(t=60, b=40))

fig_cost_breakdown = px.bar(budget.sort_values("budget_spent", ascending=False),
    x="base", y="budget_spent", color="supply_category", barmode="stack",
    title="Cost Breakdown by Base and Supply Category",
    labels={"base": "Base", "budget_spent": "Budget Spent", "supply_category": "Supply Category"})
fig_cost_breakdown.update_layout(margin=dict(t=60, b=40))

# Dash application setup
app = dash.Dash(__name__)
app.title = "Military Base Supply – Operations Insights Dashboard"

app.layout = html.Div([
    html.H2("Military Base Supply – Operations Insights", style={"textAlign": "center"}),
    html.P("Data coverage: ~90 days of simulated operational activity.", style={"textAlign": "center", "fontSize": "14px", "marginBottom": "20px"}),
    html.P("Disclaimer: This dataset is entirely fictional and does not reflect real-world military operations or supply conditions.",
    style={"textAlign": "center", "fontSize": "14px", "fontStyle": "italic", "color": "gray"}
),

    html.Div([
        html.Div([dcc.Graph(figure=fig_vendor)], style={"width": "48%", "display": "inline-block", "padding": "10px"}),
        html.Div([dcc.Graph(figure=avg_delay_fig)], style={"width": "48%", "display": "inline-block", "padding": "10px"})
    ]),

    html.Div([
        html.Div([dcc.Graph(figure=fig_severe)], style={"width": "48%", "display": "inline-block", "padding": "10px"}),
        html.Div([dcc.Graph(figure=fig_inventory)], style={"width": "48%", "display": "inline-block", "padding": "10px"})
    ]),

    html.Div([dcc.Graph(figure=fig_budget)], style={"padding": "10px"}),

    html.Div([
        html.Div([dcc.Graph(figure=fig_emergency)], style={"width": "48%", "display": "inline-block", "padding": "10px"}),
        html.Div([dcc.Graph(figure=fig_route_risk)], style={"width": "48%", "display": "inline-block", "padding": "10px"})
    ]),

    html.Div([
        html.Div([dcc.Graph(figure=fig_lead_time)], style={"width": "48%", "display": "inline-block", "padding": "10px"}),
        html.Div([dcc.Graph(figure=fig_aging)], style={"width": "48%", "display": "inline-block", "padding": "10px"})
    ]),

    html.Div([dcc.Graph(figure=fig_base_risk)], style={"padding": "10px"}),
    html.Div([dcc.Graph(figure=fig_low_inv_table)], style={"padding": "10px"}),
    html.Div([dcc.Graph(figure=fig_vendor_heatmap)], style={"padding": "10px"}),
    html.Div([dcc.Graph(figure=fig_cost_breakdown)], style={"padding": "10px"})
], style={"maxWidth": "1200px", "margin": "auto", "fontFamily": "Arial"})

if __name__ == "__main__":
    app.run(debug=True)