"""
Dashboard layout.

Author: Luis Miguel Herrera
Project: Customer Revenue Analytics
"""

from dash import html, dcc
import plotly.express as px

from queries import (
    load_kpis,
    load_monthly_revenue,
    load_category_metrics,
    load_payment_metrics,
    load_delivery_performance,
    load_customer_metrics,
)

# =============================================================================
# Load data
# =============================================================================

kpis = load_kpis()

monthly = load_monthly_revenue()

categories = load_category_metrics()

payments = load_payment_metrics()

delivery = load_delivery_performance()

customers = load_customer_metrics()


# =============================================================================
# Plot settings
# =============================================================================

plot_config = {
    "template": "plotly_white",
}


# =============================================================================
# Monthly revenue
# =============================================================================

monthly_fig = px.line(
    monthly,
    x="month",
    y="total_revenue",
    markers=True,
    title="Monthly Revenue Evolution",
    color_discrete_sequence=["#2563eb"],
)

monthly_fig.update_layout(
    **plot_config,
    margin=dict(l=20, r=20, t=60, b=20),
    title_font_size=18,
)


# =============================================================================
# Revenue by category
# =============================================================================

top_categories = categories.nlargest(
    10,
    "revenue",
).reset_index(drop=True)


# Create readable category labels
top_categories["category_display"] = (
    top_categories["product_category_name_english"]
    .str.replace("_", " ")
    .str.replace(r"\d+", "", regex=True)
    .str.strip()
    .str.title()
)


category_fig = px.bar(
    top_categories,
    x="revenue",
    y="category_display",
    orientation="h",
    title="Revenue by Product Category",
    color_discrete_sequence=["#2563eb"],
)


category_fig.update_layout(
    **plot_config,
    margin=dict(l=20, r=20, t=60, b=20),
    yaxis=dict(categoryorder="total ascending"),
    title_font_size=18,
)


# =============================================================================
# Payment methods
# =============================================================================

payment_fig = px.pie(
    payments,
    names="payment_type",
    values="total_payments",
    hole=0.55,
    title="Payment Method Distribution",
)

payment_fig.update_layout(
    **plot_config,
    margin=dict(l=20, r=20, t=60, b=20),
    title_font_size=18,
)


# =============================================================================
# Delivery performance
# =============================================================================

delivery_counts = (
    delivery["delivered_on_time"]
    .value_counts()
    .rename_axis("status")
    .reset_index(name="orders")
)

delivery_counts["status"] = delivery_counts["status"].replace(
    {
        True: "On Time",
        False: "Delayed",
    }
)

delivery_fig = px.pie(
    delivery_counts,
    names="status",
    values="orders",
    title="Delivery On-Time Performance",
    hole=0.45,
)

delivery_fig.update_layout(
    **plot_config,
    margin=dict(l=20, r=20, t=60, b=20),
    title_font_size=18,
)

# =============================================================================
# Top customers
# =============================================================================

top_customers = customers.nlargest(
    10,
    "total_spent",
).reset_index(drop=True)


# Create business-friendly labels
top_customers["customer_display"] = [
    f"Customer {i + 1}" for i in range(len(top_customers))
]


customer_fig = px.bar(
    top_customers,
    x="total_spent",
    y="customer_display",
    orientation="h",
    title="Top Customers by Spending",
    color_discrete_sequence=["#2563eb"],
)


customer_fig.update_layout(
    **plot_config,
    margin=dict(l=20, r=20, t=60, b=20),
    yaxis=dict(categoryorder="total ascending"),
    title_font_size=18,
)


# =============================================================================
# Layout
# =============================================================================

layout = html.Div(
    children=[
        # ---------------------------------------------------------
        # Header
        # ---------------------------------------------------------
        html.Div(
            children=[
                html.H1("Customer Revenue Analytics"),
                html.P(
                    "Business intelligence dashboard analyzing revenue, "
                    "customers, categories and operational performance."
                ),
            ],
            className="header",
        ),
        html.Hr(),
        # ---------------------------------------------------------
        # KPI cards
        # ---------------------------------------------------------
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H3("Total Revenue"),
                        html.H2(f"${kpis['total_revenue']:,.0f}"),
                    ],
                    className="card",
                ),
                html.Div(
                    children=[
                        html.H3("Total Orders"),
                        html.H2(f"{kpis['total_orders']:,}"),
                    ],
                    className="card",
                ),
                html.Div(
                    children=[
                        html.H3("Active Customers"),
                        html.H2(f"{kpis['total_customers']:,}"),
                    ],
                    className="card",
                ),
                html.Div(
                    children=[
                        html.H3("Average Order Value"),
                        html.H2(f"${kpis['average_order_value']:,.2f}"),
                    ],
                    className="card",
                ),
            ],
            className="kpi-container",
        ),
        html.Br(),
        # ---------------------------------------------------------
        # Monthly revenue
        # ---------------------------------------------------------
        dcc.Graph(figure=monthly_fig),
        # ---------------------------------------------------------
        # Second row
        # ---------------------------------------------------------
        html.Div(
            children=[
                dcc.Graph(figure=category_fig, style={"width": "50%"}),
                dcc.Graph(figure=payment_fig, style={"width": "50%"}),
            ],
            style={"display": "flex", "gap": "20px"},
        ),
        # ---------------------------------------------------------
        # Third row
        # ---------------------------------------------------------
        html.Div(
            children=[
                dcc.Graph(figure=delivery_fig, style={"width": "50%"}),
                dcc.Graph(figure=customer_fig, style={"width": "50%"}),
            ],
            style={"display": "flex", "gap": "20px"},
        ),
    ]
)
