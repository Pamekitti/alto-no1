import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import urllib.request, json

with urllib.request.urlopen("https://raw.githubusercontent.com/apisit/thailand.json/master/thailand.json") as url:
    json_map = json.load(url)

mapbox_access_token = 'pk.eyJ1IjoicGFtZWtpdHRpIiwiYSI6ImNsN3J1M3Q3MTBpczUzb284YXh1ZmtqMzgifQ.CqCWrWGetLG4oR3T0rrZUw'
px.set_mapbox_access_token(mapbox_access_token)

'''
1. Map
'''


# Plot Choropleth Mapbox
def plot_map_temp(df):
    fig = px.choropleth_mapbox(df, geojson=json_map, color='avg_temp',
                               locations="eng_province", featureidkey="properties.name",
                               center={"lat": 13.736717, "lon": 100.523186}, zoom=5,
                               color_continuous_scale='Viridis', range_color=[18, 32],
                               color_continuous_midpoint=28)
    fig.update_layout(mapbox_style="dark")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


def plot_map_rain(df):
    fig = px.choropleth_mapbox(df, geojson=json_map, color='rain_24h',
                               locations="eng_province", featureidkey="properties.name",
                               center={"lat": 13.736717, "lon": 100.523186}, zoom=5,
                               color_continuous_scale='GnBu', range_color=[0, 10])
    fig.update_layout(mapbox_style="dark")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


def plot_map_wind(df):
    fig = px.choropleth_mapbox(df, geojson=json_map, color='max_wind_v',
                               locations="eng_province", featureidkey="properties.name",
                               center={"lat": 13.736717, "lon": 100.523186}, zoom=5,
                               color_continuous_scale='OrRd', range_color=[0, 30])
    fig.update_layout(mapbox_style="dark")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


'''
Overview
'''


def plot_overview_month(df, province, variable):
    df = df[df['eng_province'] == province]
    fig = px.area(df, x='date', y=variable)
    fig.update_layout(template="simple_white")
    fig.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})
    fig.update_layout(
        title_text=f"{province}"
    )
    fig.update_xaxes(title_text="Date")
    variable_dict = {
        'avg_temp': ["Average Temperature (°C)", '#52BE80'],
        'rain_24h': ["Last 24 Hrs Rain", '#2980B9'],
        'max_wind_v': ["Maximum Wind Speed", '#E74C3C']
    }
    if variable == 'avg_temp':
        fig.update_layout(yaxis_range=[20, 40])
    fig.update_yaxes(title_text=variable_dict[variable][0])
    fig.update_traces(line_color=variable_dict[variable][1])
    return fig


def plot_overview_day(df, province):
    df = df[df['eng_province'] == province]
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(x=df['datetime'], y=df['temp'], name="Temperature"),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=df['datetime'], y=df['rh'], name="Relative Humidity"),
        secondary_y=True,
    )
    fig.update_layout(
        title_text="Daily Temperature vs. Relation Humidity"
    )
    fig.update_xaxes(title_text="Time")
    fig.update_yaxes(title_text="Temperature (°C)", secondary_y=False)
    fig.update_yaxes(title_text="Relative Humidity (%)", secondary_y=True)
    fig.update_layout(template="simple_white")
    return fig


def plot_wind_polar(df, province):
    df = df[df['eng_province'] == province]
    df = df.sort_values(['wind_dir', 'max_wind_v'], ascending=False)
    fig = px.bar_polar(df, r="max_wind_v", theta="wind_dir", color="max_wind_v", template="plotly_dark",
                       color_discrete_sequence=px.colors.sequential.Plasma_r)
    fig.update_layout(template="simple_white")
    return fig


def plot_wind_rain(df, province):
    df[df['eng_province'] == province]
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(x=df['date'], y=df['max_wind_v'], name="Maximum Wind Speed"),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=df['date'], y=df['rain_24h'], name="Rain Volume last 24 Hrs"),
        secondary_y=True,
    )
    fig.update_layout(
        title_text="Daily Temperature vs. Relation Humidity"
    )
    fig.update_xaxes(title_text="Time")
    fig.update_yaxes(title_text="Temperature (°C)", secondary_y=False)
    fig.update_yaxes(title_text="Relative Humidity (%)", secondary_y=True)
    fig.update_layout(template="simple_white")
    return fig
