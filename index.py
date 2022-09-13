import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Output, Input
from app import app
import os

app_port = os.environ['APP_PORT']

# Connect to the layout and callbacks of each tab
from map import map_layout
from overview import overview_layout
from explorer import explorer_layout

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

app.layout = html.Div([
    dcc.Location(id="url"),
    html.Div(
        [
            html.H2("Weather Dash", className="display-4"),
            html.Hr(),
            html.P(
                "Interactive Weather App", className="lead"
            ),
            dbc.Nav(
                [
                    dbc.NavLink("Map", href="/", active="exact"),
                    dbc.NavLink("Overview", href="/page-1", active="exact"),
                    dbc.NavLink("Data Explorer", href="/page-2", active="exact"),
                ],
                vertical=True,
                pills=True,
            ),
        ], id='sidebar',
    ),
    html.Div(id="page-content", children=[])
])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return map_layout
    elif pathname == "/page-1":
        return overview_layout
    elif pathname == "/page-2":
        return explorer_layout
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=app_port)
