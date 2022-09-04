from dash import Dash, dcc, Output, Input  # pip install dash
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import plotly.express as px
import pandas as pd                        # pip install pandas
import numpy as np
from process_thai import thai_province_map, thai_datetime

# Get Thailand map JSON File
import urllib.request, json
with urllib.request.urlopen("https://raw.githubusercontent.com/apisit/thailand.json/master/thailand.json") as url:
    json_map = json.load(url)

# Get id_table to map provinces name to ids
id_table = pd.read_csv('id_table.csv')
id_table.drop(columns=id_table.columns[0], axis=1, inplace=True)
# Table of main station in each province
id_main = id_table.drop_duplicates(subset=['id'], keep="first", inplace=False)
# Merge Names to match JSON File
df = thai_province_map(id_main, json_map)
# Merge info from main stations
current_time = pd.to_datetime('202204'
                              '09 13:00')
to_merge = []
for station_id in df['station_id']:
    if np.isnan(station_id):
        print(f'Station id: {station_id} not found')
        continue
    df_main = pd.read_csv(f'day_csv/day_{int(station_id)}.csv')
    df_main.drop(columns=df_main.columns[0], axis=1, inplace=True)
    df_main['datetime'] = df_main['datetime'].apply(lambda var: thai_datetime(var))
    df_main['station_id'] = int(station_id)
    try:
        # current_time = df_main.iloc[0,0]
        current_stat = df_main[df_main['datetime'] == current_time]
        to_merge.append(current_stat.values.tolist()[0])
        print(current_time)
    except:
        current_stat = df_main.iloc[0]
        print ('except')
        # to_merge.append(current_stat.values.tolist())
df_to_merge = pd.DataFrame(to_merge, columns=['datetime', 'temp', 'dew_point', 'rh',
                                              'pressure', 'wind_dir', 'wind_sp',
                                              'visibility', 'rain_3h', 'cloud', 'station_id'])
df = df.merge(df_to_merge, how='left', on='station_id')

# Build components
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
title = dcc.Markdown(children='')
graph = dcc.Graph(figure={})
dropdown = dcc.Dropdown(options=['temp', 'dew_point', 'rh',
                                 'pressure', 'visibility', 'rain_3h'],
                        value='temp',
                        clearable=False)

# Customize Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([title], width=6)
    ], justify='center'),
    dbc.Row([
        dbc.Col([graph], width=12)
    ]),
    dbc.Row([
        dbc.Col([dropdown], width=6)
    ], justify='center'),
], fluid=True)


# Callback allows components to interact
@app.callback(
    Output(graph, 'figure'),
    Output(title, 'children'),
    Input(dropdown, 'value')
)
def update_graph(column_name):
    print(column_name)
    print(type(column_name))
    fig = px.choropleth_mapbox(df, geojson=json_map, color=column_name,
                               locations="eng_province", featureidkey="properties.name",
                               center={"lat": 13.736717, "lon": 100.523186},
                               mapbox_style="open-street-map", zoom=4)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig, '# '+column_name


# Run app
if __name__ == '__main__':
    app.run_server(debug=True, port=8055)
