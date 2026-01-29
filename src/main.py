import dash
import dash_bootstrap_components as dbc
from dash import dcc

# Creating the Dash app
app = dash.Dash(
    __name__,
    use_pages=True,
    pages_folder="web",
    external_stylesheets=[dbc.themes.FLATLY],
)

# Creating elements for all the pages
nav_bar = dbc.NavbarSimple(
    children=dbc.Nav(
        [
            dbc.NavItem(
                dbc.NavLink(dcc.Markdown(f"###### {page['name']}"), href=page["path"]),
                id=f"tooltip-target{page['name']}",
                style={"textAlign": "center"},
            )
            for page in dash.page_registry.values()
        ],
        navbar=True,
    ),
    brand=dcc.Markdown("### Budget Management App"),
    brand_href="/",
    color="primary",
    dark=True,
)


# Defining the layout that will be used for all the pages
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(nav_bar),
            ]
        ),
        dbc.Row(dbc.Col(dash.page_container, style={"margin-top": "20px"})),
        dbc.Row(
            [
                dbc.Tooltip(
                    f"{page['description']}",
                    target=f"tooltip-target{page['name']}",
                    placement="bottom",
                )
                for page in dash.page_registry.values()
            ]
        ),
    ]
)

# Main Run of the function
if __name__ == "__main__":
    app.run(debug=True)
