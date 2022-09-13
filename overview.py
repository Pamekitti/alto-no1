import pandas as pd
from graphs.visuals import *
from dash import html, dcc
from datetime import datetime as dt
from dash.dependencies import Input, Output, State
from app import app

df_province = pd.read_csv('daily_summary/province_summary/province_all.csv')
df_province['avg_temp'] = (df_province['max_temp'] + df_province['min_temp']) / 2
df_day = pd.read_csv('assets/day_data.csv')

overview_month1 = plot_overview_month(df_province, 'Bangkok Metropolis', 'avg_temp', show_title=False)
overview_month2 = plot_overview_month(df_province, 'Bangkok Metropolis', 'rain_24h', show_title=False)
overview_month3 = plot_overview_month(df_province, 'Bangkok Metropolis', 'max_wind_v', show_title=False)
overview_day1 = plot_overview_day(df_day, 'Bangkok Metropolis', 'temp', show_title=False)
overview_day2 = plot_overview_day(df_day, 'Bangkok Metropolis', 'rh', show_title=False)
overview_day3 = plot_overview_day(df_day, 'Bangkok Metropolis', 'dew_point', show_title=False)
overview_day4 = plot_overview_day(df_day, 'Bangkok Metropolis', 'pressure', show_title=False)
overview_day5 = plot_overview_day(df_day, 'Bangkok Metropolis', 'wind_sp', show_title=False)
overview_day6 = plot_overview_day(df_day, 'Bangkok Metropolis', 'visibility', show_title=False)

province_dropdown = []
for province in df_province['eng_province']:
    province_dropdown.append({'label': province, 'value': province})

overview_layout = html.Div([
    html.H1("Weather Overview by Province "),
    html.Label("Select Province", className='dropdown-labels'),
    dcc.Dropdown(id='province-dropdown', className='dropdown',
                 options=province_dropdown,
                 value='Bangkok Metropolis'),
    html.Div([
        html.H6("Past Daily Report"),
        dcc.Graph(id='overview-month1', figure=overview_month1),
        dcc.Graph(id='overview-month2', figure=overview_month2),
        dcc.Graph(id='overview-month3', figure=overview_month3)
    ], id='left-overview'),
    html.Div([
        html.H6("Today's Hourly Report"),
        dcc.Graph(id='overview-day1', figure=overview_day1),
        dcc.Graph(id='overview-day2', figure=overview_day2),
        dcc.Graph(id='overview-day3', figure=overview_day3),
        dcc.Graph(id='overview-day4', figure=overview_day4),
        dcc.Graph(id='overview-day5', figure=overview_day5),
        dcc.Graph(id='overview-day6', figure=overview_day6),
    ], id='right-overview')
])


@app.callback(
    [Output(component_id='overview-month1',
            component_property='figure'),
     Output(component_id='overview-month2',
            component_property='figure'),
     Output(component_id='overview-month3',
            component_property='figure'),
     Output(component_id='overview-day1',
            component_property='figure'),
     Output(component_id='overview-day2',
            component_property='figure'),
     Output(component_id='overview-day3',
            component_property='figure'),
     Output(component_id='overview-day4',
            component_property='figure'),
     Output(component_id='overview-day5',
            component_property='figure'),
     Output(component_id='overview-day6',
            component_property='figure'),
     ],
    Input(component_id='province-dropdown',
          component_property='value')
)
def update_graphs(pick):
    dfp = df_province.copy()
    dfd = df_day.copy()
    fig1_1 = plot_overview_month(dfp, pick, 'avg_temp', show_title=False)
    fig1_2 = plot_overview_month(dfp, pick, 'rain_24h', show_title=False)
    fig1_3 = plot_overview_month(dfp, pick, 'max_wind_v', show_title=False)
    fig2_1 = plot_overview_day(dfd, pick, 'temp', show_title=False)
    fig2_2 = plot_overview_day(dfd, pick, 'rh', show_title=False)
    fig2_3 = plot_overview_day(dfd, pick, 'dew_point', show_title=False)
    fig2_4 = plot_overview_day(dfd, pick, 'pressure', show_title=False)
    fig2_5 = plot_overview_day(dfd, pick, 'wind_sp', show_title=False)
    fig2_6 = plot_overview_day(dfd, pick, 'visibility', show_title=False)

    return fig1_1, fig1_2, fig1_3, fig2_1, fig2_2, fig2_3, fig2_4, fig2_5, fig2_6
