from graphs.visuals import *
from dash import html, dcc
from dash.dependencies import Output, Input, State
import pandas as pd
from app import app

df = pd.read_csv('daily_summary/province_summary/province_all.csv')
df['avg_temp'] = (df['max_temp'] + df['min_temp'])/2
mapbox = plot_map_temp(df)

map_layout = html.Div([
    html.Div([
        html.Div([
            dcc.Graph(id='mapbox', figure=mapbox)
        ], id='left-container'),
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
                             value='avg_temp'),
                html.Button(id='update-button', children="Apply"),
            ]),
            html.Div([
                html.Label("Label", className='map-summary')
            ])
        ])
    ])
])


@app.callback(
    Output(component_id='mapbox',
           component_property='figure'),
    [State(component_id='map-date-range',
           component_property='value'),
     State(component_id='map-dropdown',
           component_property='value'),
     Input(component_id='update-button',
           component_property='n_clicks')
     ]
)
def update_map(date_range, data_display, n_clicks):
    dff = df.copy()
    fig = mapbox
    if n_clicks is not None:
        if n_clicks > 0:
            dff = dff[dff['date'].between(date_range[0], date_range[1])]
            if data_display == 'avg_temp':
                fig = plot_map_temp(dff)
            if data_display == 'rain_24h':
                fig = plot_map_rain(dff)
            if data_display == 'max_wind_v':
                fig = plot_map_wind(dff)
    return fig
