import dash
import dash_bootstrap_components as dbc
from dash import dcc

dash.register_page(__name__, order=2, description="View table of spending details")

# Defining the objects that will be used in the layout
p_title = dcc.Markdown("# Spending Details", style={"textAlign": "center"})

# Defining the layout
layout = dbc.Container(
    [
        dbc.Row(dbc.Col(p_title)),
    ]
)
