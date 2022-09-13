import pandas as pd
from graphs.visuals import *
from dash import html, dcc
from datetime import datetime as dt
from dash.dependencies import Input, Output, State
from app import app

df_province = pd.read_csv('daily_summary/province_summary/province_all.csv')
df_province['avg_temp'] = (df_province['max_temp'] + df_province['min_temp']) / 2
df_day = pd.read_csv('assets/day_data.csv')

overview_month1 = plot_overview_month(df_province, 'Bangkok Metropolis', 'avg_temp')
overview_month2 = plot_overview_month(df_province, 'Bangkok Metropolis', 'rain_24h')
overview_month3 = plot_overview_month(df_province, 'Bangkok Metropolis', 'max_wind_v')
overview_day = plot_overview_day(df_day, 'Bangkok Metropolis')
wine_plot = plot_wind_polar(df_province, 'Bangkok Metropolis')
wind_rain = plot_wind_rain(df_province, 'Bangkok Metropolis')

province_dropdown = []
for province in df_province['eng_province']:
    province_dropdown.append({'label': province, 'value': province})

overview_layout = html.Div([
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
    dcc.Dropdown(id='province-dropdown', className='dropdown',
                 options=province_dropdown,
                 value='Bangkok Metropolis'),
    dcc.Graph(id='overview-month1', figure=overview_month1),
    dcc.Graph(id='overview-month2', figure=overview_month2),
    dcc.Graph(id='overview-month3', figure=overview_month3),
    dcc.Graph(id='overview-day', figure=overview_day),
    dcc.Graph(id='wind-plot', figure=wine_plot),
    dcc.Graph(id='wind-rain', figure=wind_rain),
])


@app.callback(
    [Output(component_id='overview-month1',
            component_property='figure'),
     Output(component_id='overview-month2',
            component_property='figure'),
     Output(component_id='overview-month3',
            component_property='figure'),
     Output(component_id='overview-day',
            component_property='figure'),
     Output(component_id='wind-plot',
            component_property='figure'),
     Output(component_id='wind-rain',
            component_property='figure')
     ],
    [Input(component_id='my-date-picker-range',
           component_property='start_date'),
     Input(component_id='my-date-picker-range',
           component_property='end_date'),
     Input(component_id='province-dropdown',
           component_property='value')
     ]
)
def update_graphs(start, end, pick):
    dfp = df_province.copy()
    dfd = df_day.copy()
    dfp = dfp[dfp['date'].between(start, end)]
    fig1_1 = plot_overview_month(dfp, pick, 'avg_temp')
    fig1_2 = plot_overview_month(dfp, pick, 'rain_24h')
    fig1_3 = plot_overview_month(dfp, pick, 'max_wind_v')
    fig2 = plot_overview_day(dfd, pick)
    fig3 = plot_wind_polar(dfp, pick)
    fig4 = plot_wind_rain(dfp, pick)
    return fig1_1, fig1_2, fig1_3, fig2, fig3, fig4
