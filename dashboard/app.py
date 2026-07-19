"""
Customer Revenue Analytics Dashboard.

Author: Luis Miguel Herrera
Project: Customer Revenue Analytics
"""

from dash import Dash

from layout import layout


app = Dash(__name__)

app.title = "Customer Revenue Analytics"

app.layout = layout


if __name__ == "__main__":

    app.run(debug=True)