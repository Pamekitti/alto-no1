import plotly.express as px
import dash_bootstrap_components as dbc
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
import pandas as pd
from app import app


map_layout = html.Div([
    html.Div([
        html.Div([
            dcc.Graph()
        ]),
        html.Div([
            html.Div([
                html.Label("Date Range", className='dropdown-labels'),
                dcc.RangeSlider(0, 1000, id='map-date-range', value=[0, 1000],
                                tooltip={"placement": "bottom", "always_visible": True}),
                html.Label("Display Data", className='dropdown-labels'),
                dcc.Dropdown(id='map-dropdown', className='dropdown',
                             options=[
                                 {'label': 'Average Temperature', 'value': 'avg_temp'},
                                 {'label': 'Average Rain', 'value': 'rain_24h'},
                                 {'label': 'Average Wind Speed', 'value': 'max_wind_v'},
                             ],
                             value='none'),
                html.Button(id='update-button', children="Apply"),
            ]),
            html.Div([
                html.Label("Label", className='map-summary')
            ])
        ])
    ])
])
