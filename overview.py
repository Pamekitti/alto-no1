import pandas as pd
from graphs.visuals import *
from dash import html, dcc
from dash.dependencies import Input, Output, State

df_province = pd.read_csv('daily_summary/province_summary/province_all.csv')
df_day = pd.read_csv('assets/day_data.csv')

overview_month = plot_overview_month(df_province, 'Bangkok Metropolis')
overview_day = plot_overview_day(df_day, 'Bangkok Metropolis')
wine_plot = plot_wind_polar(df_province, 'Bangkok Metropolis')
wind_rain = plot_wind_rain(df_province, 'Bangkok Metropolis')

overview_layout = html.Div([
    html.Graph(id='overview-month', figure=overview_month),
    html.Graph(id='overview-day', figure=overview_day),
    html.Graph(id='wind-plot', figure=wine_plot),
    html.Graph(id='wind-rain', figure=wind_rain),
])
