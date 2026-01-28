import dash
import dash_bootstrap_components as dbc
from dash import dcc

dash.register_page(__name__, path="/", order=1, description="View budget overview")

# Defining the objects that will be used in the layout
title = dcc.Markdown("# Budget Overview", style={"textAlign": "center"})

# Get Spending Data

# Get Type of spending data

# Defining the layout
layout = dbc.Container(
    [
        dbc.Row(dbc.Col(title)),
    ]
)
