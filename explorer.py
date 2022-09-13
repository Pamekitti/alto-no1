from data_processor.process_thai import thai_datetime
from graphs.explorer_graphs import *
from graphs.visuals import *
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State, MATCH
import plotly.express as px
import pandas as pd  # pip install pandas
import numpy as np
from app import app

df = pd.read_csv('assets/main_id_table.csv')
df_province = pd.read_csv('daily_summary/province_summary/province_all.csv')
df_province['avg_temp'] = (df_province['max_temp'] + df_province['min_temp']) / 2
df_day = pd.read_csv('assets/day_data.csv')

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
                options=[
                    {'label': 'Hourly Chart', 'value': 'line_day'},
                    {'label': 'Daily Chart', 'value': 'line_province'}],
                value='line_day'
            ),
            html.Label('Select Provinces (Multiple)'),
            dcc.Dropdown(
                id={
                    'type': 'dynamic-dpn-prov',
                    'index': n_clicks
                },
                options=[{'label': s, 'value': s} for s in np.sort(df['eng_province'].unique())],
                multi=True,
                value=["Bangkok Metropolis", "Rayong", "Chiang Mai"], 
            ),
            html.Label('Select data for hourly chart'),
            dcc.Dropdown(
                id={
                    'type': 'dynamic-dpn-val-day',
                    'index': n_clicks
                },
                options=[
                    {'label': "Temperature (°C)", 'value': 'temp'},
                    {'label': "Dew Point", 'value': 'dew_point'},
                    {'label': "Relative Humidity", 'value': 'rh'},
                    {'label': "Pressure", 'value': 'pressure'},
                    {'label': "Wind Speed", 'value': 'wind_sp'},
                    {'label': "Visibility", 'value': 'visibility'},
                    {'label': "Rain in 3 Hrs", 'value': 'rain_3h'}
                ],
                value='temp',
                clearable=False

            ),
            html.Label('Select data for daily chart'),
            dcc.Dropdown(
                id={
                    'type': 'dynamic-dpn-val-province',
                    'index': n_clicks
                },
                options=[
                    {'label': "Average Temperature", 'value': 'avg_temp'},
                    {'label': "Last 24 Hrs Rain", 'value': 'rain_24h'},
                    {'label': "Maximum Wind Speed", 'value': 'max_wind_v'},
                         ],
                value='avg_temp',
                clearable=False
            )
        ]
    )
    div_children.append(new_child)
    return div_children


@app.callback(
    Output({'type': 'dynamic-graph', 'index': MATCH}, 'figure'),
    [Input(component_id={'type': 'dynamic-dpn-prov', 'index': MATCH}, component_property='value'),
     Input(component_id={'type': 'dynamic-dpn-val-day', 'index': MATCH}, component_property='value'),
     Input(component_id={'type': 'dynamic-dpn-val-province', 'index': MATCH}, component_property='value'),
     Input({'type': 'dynamic-choice', 'index': MATCH}, 'value')]
)
def update_graph(prov_value, day_val,province_val, chart_choice):
    print(prov_value)

    dfd = df_day[df_day['eng_province'].isin(prov_value)]
    dfp = df_province[df_province['eng_province'].isin(prov_value)]

    if chart_choice == 'line_day':
        fig = line_plot_day(dfd, day_val)
        return fig
    elif chart_choice == 'line_province':
        fig = line_plot_province(dfp, province_val)
        return fig
