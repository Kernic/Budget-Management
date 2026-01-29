import datetime

import dash
import dash_bootstrap_components as dbc
import pandas as pds
import plotly.graph_objects as go
from dash import dcc

from data.db import get_value, get_values_as_dataframe

dash.register_page(__name__, path="/", order=1, description="View budget overview")

# Defining the objects that will be used in the layout
title = dcc.Markdown("## Budget Overview", style={"textAlign": "center"})

# Getting current balance
bal_val = get_value("SELECT value FROM global_values WHERE key = 'balance'")
bal_card = dbc.Card(
    [
        dbc.CardHeader(dcc.Markdown("#### Balance")),
        dbc.CardBody(dcc.Markdown(f"##### {bal_val} €", style={"textAlign": "center"})),
    ],
    color="primary",
    inverse=True,
)

last_update = get_value(
    "SELECT value FROM global_values WHERE key = 'last_update_date'"
)
last_update_card = dbc.Card(
    [
        dbc.CardHeader(dcc.Markdown("#### Last Update")),
        dbc.CardBody(
            dcc.Markdown(f"##### {last_update}", style={"textAlign": "center"})
        ),
    ],
    color="info",
    inverse=True,
)

older_date = get_value("SELECT value FROM global_values WHERE key = 'oldest_date'")
older_date_card = dbc.Card(
    [
        dbc.CardHeader(dcc.Markdown("#### Oldest Date")),
        dbc.CardBody(
            dcc.Markdown(f"##### {older_date}", style={"textAlign": "center"})
        ),
    ],
    color="secondary",
    inverse=True,
)

# Month Balance Card
month_bal_dts = float(
    get_value(
        "SELECT SUM(amount) FROM operations WHERE strftime('%Y', date) = strftime('%Y', 'now') AND strftime('%m', date) = strftime('%m', 'now');"
    )
)
month_dts_card = dbc.Card(
    [
        dbc.CardHeader(dcc.Markdown("#### Month Balance")),
        dbc.CardBody(
            dcc.Markdown(f"##### {month_bal_dts:.2f} €", style={"textAlign": "center"})
        ),
    ],
    color=(
        "success"
        if month_bal_dts >= 500
        else "warning"
        if month_bal_dts >= 0
        else "danger"
    ),
    inverse=True,
)

# Get Spending Data
dts = get_values_as_dataframe("SELECT * FROM operations;")
dts["date"] = pds.to_datetime(dts["date"])
grouped_dts = dts.groupby("date").agg(results=("amount", "sum")).reset_index()
grouped_dts["color"] = grouped_dts["results"].apply(
    lambda x: "lightgreen" if x > 0 else "lightcoral"
)
grouped_dts = grouped_dts.sort_values("date", ascending=False)
bal_evol = [float(bal_val)]
for i in range(1, len(grouped_dts)):
    bal_evol.append(bal_evol[i - 1] - grouped_dts["results"].iloc[i - 1])
grouped_dts["date_balance"] = bal_evol
operations_fig = go.Figure()
operations_fig.add_trace(
    go.Bar(
        x=grouped_dts["date"],
        y=grouped_dts["results"],
        marker_color=grouped_dts["color"],
        name="Spending",
    )
)
operations_fig.add_trace(
    go.Scatter(
        x=grouped_dts["date"],
        y=grouped_dts["date_balance"],
        mode="lines+markers",
        line=dict(color="black", width=2),
        line_shape="spline",
        name="Balance",
    )
)
operations_fig.update_layout(title="Spending Over Time")
operations_fig.update_xaxes(
    type="date",
    range=[
        datetime.datetime.strptime(last_update, "%d/%m/%Y")
        - datetime.timedelta(days=30),
        datetime.datetime.strptime(last_update, "%d/%m/%Y"),
    ],
)
operations_fig.update_yaxes(
    title="Balance (€)",
    tickformat=".2f",
    range=[
        grouped_dts[grouped_dts["date"].dt.month == datetime.datetime.now().month][
            "results"
        ].min()
        - 100,
        grouped_dts[grouped_dts["date"].dt.month == datetime.datetime.now().month][
            "date_balance"
        ].max()
        + 100,
    ],
)

graph_object = dcc.Graph(figure=operations_fig)

# Get Type of spending data

month_dts_pie = get_values_as_dataframe(
    "SELECT * FROM operations WHERE strftime('%Y', date) = strftime('%Y', 'now') AND strftime('%m', date) = strftime('%m', 'now') AND amount < 0;"
)
month_dts_pie["amount"] = month_dts_pie["amount"].abs()


type_grouped = (
    month_dts_pie.groupby(["category"]).agg(results=("amount", "sum")).reset_index()
)
pie_chart = go.Figure()
pie_chart.add_trace(
    go.Pie(
        labels=type_grouped["category"],
        values=type_grouped["results"],
    )
)
pie_chart.update_layout(title="Spending by Type")

pie_chart_object = dcc.Graph(figure=pie_chart)


month_dts_bar = get_values_as_dataframe(
    "SELECT * FROM operations WHERE strftime('%Y', date) = strftime('%Y', 'now') AND strftime('%m', date) = strftime('%m', 'now');"
)

month_dts_bar_grouped = (
    month_dts_bar.groupby(["category"]).agg(results=("amount", "sum")).reset_index()
)

month_dts_bar_grouped["color"] = month_dts_bar_grouped["results"].apply(
    lambda x: "lightgreen" if x > 0 else "lightcoral"
)

bar_chart = go.Figure()
bar_chart.add_trace(
    go.Bar(
        y=month_dts_bar_grouped["category"],
        x=month_dts_bar_grouped["results"],
        marker_color=month_dts_bar_grouped["color"],
        orientation="h",
    )
)
bar_chart.update_layout(title="Budget by Category")

bar_chart_object = dcc.Graph(figure=bar_chart)

# Defining the layout
layout = dbc.Container(
    [
        dbc.Alert(
            f"Viewing Budget for the month {datetime.datetime.now().strftime('%B %Y')}",
            color="info",
            dismissable=True,
            duration=4000,
        ),
        dbc.Row(dbc.Col(title)),
        dbc.Row(
            [
                dbc.Col(last_update_card, style={"margin-top": "10px"}),
                dbc.Col(older_date_card, style={"margin-top": "10px"}),
                dbc.Col(bal_card, style={"margin-top": "10px"}),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(month_dts_card, style={"margin-top": "10px"}),
            ]
        ),
        dbc.Row([dbc.Col(pie_chart_object), dbc.Col(bar_chart_object)]),
        dbc.Row(dbc.Col(graph_object)),
    ]
)
