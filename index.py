import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Output, Input
from app import app

# Connect to the layout and callbacks of each tab
from map import map_layout
from overview import overview_layout
from explorer import explorer_layout

app_tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label='Map', tab_id='tab-map', labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
                dbc.Tab(label='Overview', tab_id='tab-overview', labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
                # dbc.Tab(label='Data Explorer', tab_id='tab-explorer', labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger")
            ],
            id="tabs",
            active_tab="tab-map",
        ),
    ], className="mt-3"
)

app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("Weather Dash", style={"textAlign": "center"}), width=12)),
    dbc.Row(dbc.Col(app_tabs, width=12), className="mb-3"),
    html.Div(id='content', children=[])
])


@app.callback(
    [Output(component_id="content",
            component_property="children")],
    [Input(component_id="tabs",
           component_property="active_tab")]
)
def switch_tab(tab_chosen):
    if tab_chosen == "tab-map":
        return map_layout
    if tab_chosen == "tab-overview":
        return overview_layout
    # if tab_chosen == "tab-explorer":
    #     return explorer_layout


if __name__ == '__main__':
    app.run_server(debug=True, port=80)


