import dash
from dash import dcc, html
from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
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
current_time = pd.to_datetime('202204' '09 13:00')
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

app = dash.Dash(__name__)

app.layout = html.Div([
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
        style={'width': '45%', 'display': 'inline-block', 'outline': 'thin lightgrey solid', 'padding': 10},
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
                options=[{'label': 'Choropleth Map', 'value': 'choropleth'},
                         {'label': 'Bar Chart', 'value': 'bar'}],
                value='bar',
            ),
            dcc.Dropdown(
                id={
                    'type': 'dynamic-dpn-prov',
                    'index': n_clicks
                },
                options=[{'label': s, 'value': s} for s in np.sort(df['eng_province'].unique())],
                multi=True,
                value=["Bangkok Metropolis", "Rayong"],
            ),
            dcc.Dropdown(
                id={
                    'type': 'dynamic-dpn-val',
                    'index': n_clicks
                },
                options=[{'label': c, 'value': c} for c in ['temp', 'dew_point', 'rh',
                                                            'pressure', 'visibility', 'rain_3h']],
                value='temp',
                clearable=False
            )
        ]
    )
    div_children.append(new_child)
    return div_children


@app.callback(
Output({'type': 'dynamic-graph', 'index': MATCH}, 'figure'),
    [Input(component_id={'type': 'dynamic-dpn-prov', 'index': MATCH}, component_property='value'),
     Input(component_id={'type': 'dynamic-dpn-val', 'index': MATCH}, component_property='value'),
     Input({'type': 'dynamic-choice', 'index': MATCH}, 'value')]
)
def update_graph(prov_value, val_value, chart_choice):
    print(prov_value)
    dff = df[df['eng_province'].isin(prov_value)]

    if chart_choice == 'choropleth':
        fig = px.choropleth_mapbox(df, geojson=json_map, color=val_value,
                                   locations="eng_province", featureidkey="properties.name",
                                   center={"lat": 13.736717, "lon": 100.523186},
                                   mapbox_style="open-street-map", zoom=4)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return fig
    elif chart_choice == 'bar':
        fig = px.bar(dff, x='eng_province', y=val_value,
                     hover_data=['temp', 'rh', 'pressure', 'rain_3h'], color='temp',
                     labels={'eng_province': 'Province'}, height=400)
        return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8000)