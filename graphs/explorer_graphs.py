import plotly.express as px
import urllib.request, json

with urllib.request.urlopen("https://raw.githubusercontent.com/apisit/thailand.json/master/thailand.json") as url:
    json_map = json.load(url)

mapbox_access_token = 'pk.eyJ1IjoicGFtZWtpdHRpIiwiYSI6ImNsN3J1M3Q3MTBpczUzb284YXh1ZmtqMzgifQ.CqCWrWGetLG4oR3T0rrZUw'
px.set_mapbox_access_token(mapbox_access_token)

'''
Functions to generate graphs for explorer.py or Data Explorer page on DASH Web
'''

def line_plot_day(df, variable):
    fig = px.line(df, x="datetime", y=variable, color='eng_province')
    fig.update_layout(template="simple_white")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_xaxes(title_text="Datetime")
    variable_dict = {
        'temp': "Temperature (°C)",
        'dew_point': "Dew Point",
        'rh': "Relative Humidity",
        'pressure': "Pressure",
        'wind_sp': "Wind Speed",
        'visibility': "Visibility",
        'rain_3h': "Rain in 3 Hrs",
    }
    if variable == 'temp':
        fig.update_layout(yaxis_range=[20, 40])
    fig.update_yaxes(title_text=variable_dict[variable])
    return fig


def line_plot_province(df, variable):
    fig = px.line(df, x="date", y=variable, color='eng_province')
    fig.update_layout(template="simple_white")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    variable_dict = {
        'avg_temp': "Average Temperature",
        'rain_24h': "Last 24 Hrs Rain",
        'max_wind_v': "Maximum Wind Speed",
    }
    if variable == 'avg_temp':
        fig.update_layout(yaxis_range=[20, 40])
    fig.update_yaxes(title_text=variable_dict[variable])
    return fig
