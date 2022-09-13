import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Output, Input
from app import app

# Connect to the layout and callbacks of each tab
from map import map_layout
from overview import overview_layout
from explorer import explorer_layout

# app_tabs = html.Div(
#     [
#         dbc.Tabs(
#             [
#                 dbc.Tab(label='Map', tab_id='tab-map', labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
#                 dbc.Tab(label='Overview', tab_id='tab-overview', labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
#                 dbc.Tab(label='Data Explorer', tab_id='tab-explorer', labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger")
#             ],
#             id="tabs",
#             active_tab="tab-map",
#         ),
#     ], className="mt-3"
# )
#
# app.layout = dbc.Container([
#     dbc.Row(dbc.Col(html.H1("Weather Dash", style={"textAlign": "center"}), width=12)),
#     dbc.Row(dbc.Col(app_tabs, width=12), className="mb-3"),
#     html.Div(id='content', children=[])
# ])
#
#
# @app.callback(
#     Output(component_id="content",
#            component_property="children"),
#     [Input(component_id="tabs",
#            component_property="active_tab")]
# )
# def switch_tab(tab_chosen):
#     if tab_chosen == "tab-map":
#         return map_layout
#     if tab_chosen == "tab-overview":
#         return overview_layout
#     if tab_chosen == "tab-explorer":
#         return explorer_layout
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

sidebar = html.Div(
    [
        html.H2("Weather Dash", className="display-4"),
        html.Hr(),
        html.P(
            "Interactive Weather Visualization Platform", className="lead"
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
    ],style=SIDEBAR_STYLE,
)
content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
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
    app.run_server(debug=True, port=8080)


