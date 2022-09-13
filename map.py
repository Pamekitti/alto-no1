from graphs.visuals import *
from dash import html, dcc
from dash.dependencies import Output, Input, State
import pandas as pd
from datetime import datetime as dt
from app import app

df = pd.read_csv('daily_summary/province_summary/province_all.csv')
df['avg_temp'] = (df['max_temp'] + df['min_temp']) / 2
mapbox = plot_map_temp(df)
overview_month = plot_overview_month(df, 'Bangkok Metropolis', 'avg_temp')

map_layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                dcc.Graph(id='mapbox', figure=mapbox, hoverData={'points': [{'location': 'Bangkok Metropolis'}]})
            ], id='left-container'),
            html.Div([
                html.H1("Weather Map"),
                html.P("Hover over your province of interest on the map to view weather time-series "
                       "and summary based on selected data to display"),
                html.Label("Date Range", className='dropdown-labels', id='date-range'),
                dcc.DatePickerRange(
                    id='my-date-picker-range',  # ID to be used for callback
                    calendar_orientation='horizontal',  # vertical or horizontal
                    day_size=39,  # size of calendar image. Default is 39
                    end_date_placeholder_text="Return",  # text that appears when no end date chosen
                    with_portal=False,  # if True calendar will open in a full screen overlay portal
                    first_day_of_week=0,  # Display of calendar when open (0 = Sunday)
                    reopen_calendar_on_clear=True,
                    is_RTL=False,  # True or False for direction of calendar
                    clearable=True,  # whether or not the user can clear the dropdown
                    number_of_months_shown=1,  # number of months shown when calendar is open
                    min_date_allowed=dt(2022, 7, 1),  # minimum date allowed on the DatePickerRange component
                    max_date_allowed=dt(2022, 9, 11),  # maximum date allowed on the DatePickerRange component
                    initial_visible_month=dt(2022, 8, 1),
                    # the month initially presented when the user opens the calendar
                    start_date=dt(2022, 7, 1).date(),
                    end_date=dt(2022, 9, 11).date(),
                    display_format='MMM Do, YY',  # how selected dates are displayed in the DatePickerRange component.
                    month_format='MMMM, YYYY',  # how calendar headers are displayed when the calendar is opened.
                    minimum_nights=2,  # minimum number of days between start and end date

                    persistence=True,
                    persisted_props=['start_date'],
                    persistence_type='session',
                    updatemode='singledate'
                ),
                html.Label("Display Data", className='dropdown-labels'),
                dcc.Dropdown(id='map-dropdown', className='dropdown',
                             options=[
                                 {'label': 'Average Temperature', 'value': 'avg_temp'},
                                 {'label': 'Average Rain', 'value': 'rain_24h'},
                                 {'label': 'Average Wind Speed', 'value': 'max_wind_v'},
                             ],
                             value='avg_temp'),
                html.Label("Province Summary", className='map-summary'),
                dcc.Graph(id='map-fig-1', figure=overview_month),
            ], id='right-container')
        ], id='main-container')
    ])
])


@app.callback(
    [Output(component_id='mapbox',
            component_property='figure'),
     Output(component_id='map-fig-1',
            component_property='figure')],
    [Input(component_id='my-date-picker-range',
           component_property='start_date'),
     Input(component_id='my-date-picker-range',
           component_property='end_date'),
     Input(component_id='map-dropdown',
           component_property='value'),
     Input(component_id='mapbox',
           component_property='hoverData')
     ]
)
def update_map(start, end, data_display, hover):
    dff = df.copy()
    dff = dff[dff['date'].between(start, end)]
    if data_display == 'avg_temp':
        fig1 = plot_map_temp(dff)
    if data_display == 'rain_24h':
        fig1 = plot_map_rain(dff)
    if data_display == 'max_wind_v':
        fig1 = plot_map_wind(dff)
    return fig1, plot_overview_month(dff, hover['points'][0]['location'], data_display)
