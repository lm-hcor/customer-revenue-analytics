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
# Monthly revenue
# =============================================================================

monthly_fig = px.line(
    monthly,
    x="month",
    y="total_revenue",
    markers=True,
    title="Monthly Revenue",
)

monthly_fig.update_layout(
    template="plotly_white",
    margin=dict(l=20, r=20, t=60, b=20),
)

# =============================================================================
# Top categories
# =============================================================================

top_categories = categories.nlargest(10, "revenue")

category_fig = px.bar(
    top_categories,
    x="revenue",
    y="product_category_name_english",
    orientation="h",
    title="Top Categories by Revenue",
)

category_fig.update_layout(
    template="plotly_white",
    margin=dict(l=20, r=20, t=60, b=20),
    yaxis=dict(categoryorder="total ascending"),
)

# =============================================================================
# Payment methods
# =============================================================================

payment_fig = px.pie(
    payments,
    names="payment_type",
    values="total_payments",
    hole=0.55,
    title="Payment Methods",
)

payment_fig.update_layout(
    template="plotly_white",
    margin=dict(l=20, r=20, t=60, b=20),
)

# =============================================================================
# Delivery performance
# =============================================================================

delivery_fig = px.pie(
    delivery,
    names="delivery_status",
    values="total_orders",
    title="Delivery Performance",
)

delivery_fig.update_layout(
    template="plotly_white",
    margin=dict(l=20, r=20, t=60, b=20),
)

# =============================================================================
# Top customers
# =============================================================================

top_customers = customers.nlargest(
    10,
    "total_spent",
)

customer_fig = px.bar(
    top_customers,
    x="total_spent",
    y="customer_unique_id",
    orientation="h",
    title="Top Customers",
)

customer_fig.update_layout(
    template="plotly_white",
    margin=dict(l=20, r=20, t=60, b=20),
    yaxis=dict(categoryorder="total ascending"),
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

                html.H1(
                    "Customer Revenue Analytics Dashboard"
                ),

                html.P(
                    "Interactive dashboard built with Python, PostgreSQL and Dash."
                )

            ],

            className="header"

        ),

        html.Hr(),

        # ---------------------------------------------------------
        # KPI cards
        # ---------------------------------------------------------

        html.Div(

            children=[

                html.Div(

                    children=[

                        html.H3("Revenue"),

                        html.H2(f"${kpis['revenue']:,.0f}")

                    ],

                    className="card"

                ),

                html.Div(

                    children=[

                        html.H3("Orders"),

                        html.H2(f"{kpis['total_orders']:,}")

                    ],

                    className="card"

                ),

                html.Div(

                    children=[

                        html.H3("Customers"),

                        html.H2(f"{kpis['total_customers']:,}")

                    ],

                    className="card"

                ),

                html.Div(

                    children=[

                        html.H3("Average Order"),

                        html.H2(f"${kpis['average_order_value']:,.2f}")

                    ],

                    className="card"

                ),

            ],

            className="kpi-container"

        ),

        html.Br(),

        # ---------------------------------------------------------
        # Monthly revenue
        # ---------------------------------------------------------

        dcc.Graph(
            figure=monthly_fig
        ),

        # ---------------------------------------------------------
        # Second row
        # ---------------------------------------------------------

        html.Div(

            children=[

                dcc.Graph(
                    figure=category_fig,
                    style={"width": "50%"}
                ),

                dcc.Graph(
                    figure=payment_fig,
                    style={"width": "50%"}
                )

            ],

            style={

                "display": "flex",

                "gap": "20px"

            }

        ),

        # ---------------------------------------------------------
        # Third row
        # ---------------------------------------------------------

        html.Div(

            children=[

                dcc.Graph(
                    figure=delivery_fig,
                    style={"width": "50%"}
                ),

                dcc.Graph(
                    figure=customer_fig,
                    style={"width": "50%"}
                )

            ],

            style={

                "display": "flex",

                "gap": "20px"

            }

        )

    ]

)