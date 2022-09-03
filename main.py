from dash import Dash, dcc, Output, Input  # pip install dash
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import plotly.express as px
import pandas as pd                        # pip install pandas
import numpy as np

# Get Thailand map JSON File
import urllib.request, json
with urllib.request.urlopen("https://raw.githubusercontent.com/apisit/thailand.json/master/thailand.json") as url:
    data = json.load(url)
eng_list = []
for i in range(77):
    eng_list.append(data['features'][i]['properties']['name'])

'''
Get id_table to map provinces name to ids
'''
id_table = pd.read_csv('id_table.csv')
id_table.drop(columns=id_table.columns[0], axis=1, inplace=True)
# Table of main station in each province
id_main = id_table.drop_duplicates(subset=['id'], keep="first", inplace=False)

'''
Map province name from Thai to English
'''
name_map = pd.read_csv('Provinces_of_Thailand_1.csv')

name_map[['province', 'eng_province']] = name_map[['Name\n(in Thai)', 'Namesake town/city']]
mapper = name_map[['province', 'eng_province']]
index = mapper[mapper['eng_province']=='Bangkok'].index
mapper.loc[index, 'eng_province'] = 'Bangkok Metropolis'

index = mapper[mapper['eng_province']=='Buriram'].index
mapper.loc[index, 'eng_province'] = 'Buri Ram'

index = mapper[mapper['eng_province']=='Chonburi'].index
mapper.loc[index, 'eng_province'] = 'Chon Buri'

index = mapper[mapper['eng_province']=='Lopburi'].index
mapper.loc[index, 'eng_province'] = 'Lop Buri'

index = mapper[mapper['eng_province']=='Phang Nga'].index
mapper.loc[index, 'eng_province'] = 'Phangnga'

index = mapper[mapper['eng_province']=='Prachinburi'].index
mapper.loc[index, 'eng_province'] = 'Prachin Buri'

index = mapper[mapper['eng_province']=='Sisaket'].index
mapper.loc[index, 'eng_province'] = 'Si Sa Ket'

index = mapper[mapper['eng_province']=='Sukhothai (Sukhothai Thani)'].index
mapper.loc[index, 'eng_province'] = 'Sukhothai'

# Merge Names to match JSON File
dfth = pd.DataFrame({'eng_province': eng_list})
dfth = dfth.merge(mapper, how='left', on='eng_province')
dfth = dfth.merge(id_main, how='left', on='province')

from dateutil.relativedelta import relativedelta
def thai_datetime(test_str):
    test_str = test_str.replace(' น.', '')
    test_str = test_str.replace(' ม.ค. ', '01')
    test_str = test_str.replace(' ก.พ. ', '02')
    test_str = test_str.replace(' มี.ย. ', '03')
    test_str = test_str.replace(' เม.ย. ', '04')
    test_str = test_str.replace(' พ.ค. ', '05')
    test_str = test_str.replace(' มิ.ย. ', '06')
    test_str = test_str.replace(' ก.ค. ', '07')
    test_str = test_str.replace(' ส.ค. ', '08')
    test_str = test_str.replace(' ก.ย. ', '09')
    test_str = test_str.replace(' ต.ค. ', '10')
    test_str = test_str.replace(' พ.ย. ', '11')
    test_str = test_str.replace(' ธ.ค. ', '12')

    test_str = pd.to_datetime(test_str) - relativedelta(years=43)
    return test_str

# Merge info from main stations
current_time = pd.to_datetime('20220209 22:00')
to_merge = []
for station_id in dfth['station_id']:
    if np.isnan(station_id):
        print(f'Station id: {station_id} not found')
        continue
    df_main = pd.read_csv(f'day_csv/day_{int(station_id)}.csv')
    df_main.drop(columns=df_main.columns[0], axis=1, inplace=True)
    df_main['datetime'] = df_main['datetime'].apply(lambda var: thai_datetime(var))
    df_main['station_id'] = int(station_id)
    try:
        current_stat = df_main[df_main['datetime']==current_time]
        to_merge.append(current_stat.values.tolist()[0])
    except:
        current_stat = df_main.iloc[0]
        # to_merge.append(current_stat.values.tolist())
df_to_merge = pd.DataFrame(to_merge, columns=current_stat.columns)
dfth = dfth.merge(df_to_merge, how='left', on='station_id')

# Build components
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
mytitle = dcc.Markdown(children='')
mygraph = dcc.Graph(figure={})
dropdown = dcc.Dropdown(options=dfth.columns.values[2:],
                        value='temp',
                        clearable=False)

# Customize Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([mytitle], width=6)
    ], justify='center'),
    dbc.Row([
        dbc.Col([mygraph], width=12)
    ]),
    dbc.Row([
        dbc.Col([dropdown], width=6)
    ], justify='center'),
], fluid=True)

# Callback allows components to interact
@app.callback(
    Output(mygraph, 'figure'),
    Output(mytitle, 'children'),
    Input(dropdown, 'value')
)
def update_graph(column_name):
    print(column_name)
    print(type(column_name))
    fig = px.choropleth_mapbox(dfth, geojson=data, color="temp",
                               locations="eng_province", featureidkey="properties.name",
                               center={"lat": 13.736717, "lon": 100.523186},
                               mapbox_style="open-street-map", zoom=4)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig, '# '+column_name

# Run app
if __name__=='__main__':
    app.run_server(debug=True, port=8055)