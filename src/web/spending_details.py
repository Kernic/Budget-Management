import datetime as dt

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, callback, dash_table, dcc

from data.db import get_values_as_dataframe
from web.overview import last_update

dash.register_page(__name__, order=2, description="View table of spending details")

# Defining the objects that will be used in the layout
p_title = dcc.Markdown("## Spending Details", style={"textAlign": "center"})
start_date = dt.datetime.strptime(last_update, "%d/%m/%Y") - dt.timedelta(days=30)
end_date = dt.datetime.strptime(last_update, "%d/%m/%Y")
date_range_picker = dcc.DatePickerRange(
    id="date-range-picker",
    start_date=start_date,
    end_date=end_date,
)

# getting spending table

table = dash_table.DataTable(
    id="spending-table",
    hidden_columns=["id"],
    style_cell={"white-space": "pre-line"},
    editable=True,
    page_size=10,
)

# Defining the layout
layout = dbc.Container(
    [
        dbc.Row(dbc.Col(p_title)),
        dbc.Row(dbc.Col(date_range_picker, style={"textAlign": "center"})),
        dbc.Row(dbc.Col(table), style={"margin-bottom": "60px"}),
    ]
)


@callback(
    Output("spending-table", "data"),
    Input("date-range-picker", "start_date"),
    Input("date-range-picker", "end_date"),
)
def update_spending_table(start_date, end_date):
    return get_values_as_dataframe(
        f"SELECT * FROM operations WHERE date BETWEEN '{start_date}' AND '{end_date}'"
    ).to_dict("records")


# Printing the id of the selected row
@callback(Input("spending-table", "active_cell"), Input("spending-table", "data"))
def print_selected_row_id(active_cell, data):
    print(data[active_cell["row"]])
    # df = pds.DataFrame(data).iloc[:, active_cell["row"]]
    # print(df)
