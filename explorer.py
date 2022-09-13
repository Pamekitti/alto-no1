from data_processor.process_thai import thai_datetime
from graphs.plot_error_mode import plot_line_error
import dash
from dash import dcc, html
from graphs.visuals import *
from dash.dependencies import Input, Output, State, MATCH
import plotly.express as px
import pandas as pd                        # pip install pandas
import numpy as np
from app import app

df = pd.read_csv('assets/main_id_table.csv')
df_day = pd.read_csv('assets/day_data.csv')
df_week = pd.read_csv('assets/week_data.csv')

explorer_layout = html.Div([
    html.Div(children=[
        html.Button('Add Chart', id='add-chart', n_clicks=0)
    ]),
    html.Div(id='container', children=[])
])


@app.callback(
    Output(component_id='container', component_property='children'),
    [Input(component_id='add-chart', component_property='n_clicks')],
    [State(component_id='container', component_property='children')]
)
def display_graphs(n_clicks, div_children):
    new_child = html.Div(
        style={'width': '100%', 'display': 'inline-block', 'outline': 'thin lightgrey solid', 'padding': 10},
        children=[
            dcc.Graph(
                id={
                    'type': 'dynamic-graph',
                    'index': n_clicks
                },
                figure={}
            ),
            dcc.RadioItems(
                id={
                    'type': 'dynamic-choice',
                    'index': n_clicks
                },
                options=[{'label': 'Choropleth Map', 'value': 'choropleth'},
                         {'label': 'Line Day Chart', 'value': 'line_day'},
                         {'label': 'Line Week Chart', 'value': 'line_week'}],
                value='choropleth',
            ),
            dcc.Dropdown(
                id={
                    'type': 'dynamic-dpn-prov',
                    'index': n_clicks
                },
                options=[{'label': s, 'value': s} for s in np.sort(df['eng_province'].unique())],
                multi=True,
                value=["Bangkok Metropolis", "Rayong", "Chiang Mai"],
            ),
            dcc.Dropdown(
                id={
                    'type': 'dynamic-dpn-val',
                    'index': n_clicks
                },
                options=[{'label': c, 'value': c} for c in ['temp', 'dew_point', 'rh',
                                                            'pressure', 'visibility', 'rain_3h']],
                value='temp',
                clearable=False
            )
        ]
    )
    div_children.append(new_child)
    return div_children


@app.callback(
    Output({'type': 'dynamic-graph', 'index': MATCH}, 'figure'),
    [Input(component_id={'type': 'dynamic-dpn-prov', 'index': MATCH}, component_property='value'),
     Input(component_id={'type': 'dynamic-dpn-val', 'index': MATCH}, component_property='value'),
     Input({'type': 'dynamic-choice', 'index': MATCH}, 'value')]
)
def update_graph(prov_value, val_value, chart_choice):
    print(prov_value)
    current_time = thai_datetime('04 ก.ย. 65 13:00 น.')

    dff_day = df_day[df_day['eng_province'].isin(prov_value)]
    dff_now = dff_day[dff_day['datetime'] == current_time]

    dff_week = df_week[df_week['eng_province'].isin(prov_value)]

    if chart_choice == 'choropleth':
        fig = px.choropleth_mapbox(df_day, geojson=json_map, color=val_value,
                                   locations="eng_province", featureidkey="properties.name",
                                   center={"lat": 13.736717, "lon": 100.523186}, zoom=4)
        fig.update_layout(mapbox_style="dark")
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return fig
    elif chart_choice == 'line_day':
        fig = px.line(dff_day, x="datetime", y=val_value, color='eng_province')
        fig.update_layout(template="simple_white")
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return fig
    elif chart_choice == 'line_week':
        dff_week['temp_error'] = (dff_week['max_temp'] - dff_week['min_temp']) / 2
        dff_week['mean_temp'] = dff_week['min_temp'] + dff_week['temp_error']
        fig = plot_line_error(error_y_mode='band', data_frame=dff_week, x='date',
                              y='mean_temp', error_y='temp_error', color='eng_province')
        fig.update_layout(template="simple_white")
        # fig = px.line(dff_week, x="date", y='mean_temp', color='eng_province')
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return fig
