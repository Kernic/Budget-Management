import dash
import dash_bootstrap_components as dbc
from dash import dcc

dash.register_page(__name__, order=9, description="Upload new data using CSV file")

# Defining the objects that will be used in the layout
p_title = dcc.Markdown("# Upload New Data", style={"textAlign": "center"})

# Defining the layout
layout = dbc.Container(
    [
        dbc.Row(dbc.Col(p_title)),
    ]
)
