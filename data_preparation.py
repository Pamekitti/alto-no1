from data_processor.process_thai import thai_province_map, thai_datetime
import urllib.request, json
import pandas as pd
import numpy as np

with urllib.request.urlopen("https://raw.githubusercontent.com/apisit/thailand.json/master/thailand.json") as url:
    json_map = json.load(url)


# Get id_table to map provinces name to ids
id_table = pd.read_csv('assets/id_table.csv')
id_table.drop(columns=id_table.columns[0], axis=1, inplace=True)
# Table of main station in each province
id_main = id_table.drop_duplicates(subset=['id'], keep="first", inplace=False)
# Merge Names to match JSON File
df = thai_province_map(id_main, json_map)

'''
Prepare Data for Dashboard
'''
# Day Data
to_merge = []
for station_id in df['station_id']:
    if np.isnan(station_id):
        print(f'Station id: {station_id} not found')
        continue
    df_main = pd.read_csv(f'station_summary/day_csv/day_{int(station_id)}.csv')
    df_main.drop(columns=df_main.columns[0], axis=1, inplace=True)
    df_main['datetime'] = df_main['datetime'].apply(lambda var: thai_datetime(var))
    df_main['station_id'] = int(station_id)
    to_merge += df_main.values.tolist()
df_to_merge = pd.DataFrame(to_merge, columns=['datetime', 'temp', 'dew_point', 'rh',
                                              'pressure', 'wind_dir', 'wind_sp',
                                              'visibility', 'rain_3h', 'cloud', 'station_id'])
df_day = df.merge(df_to_merge, how='left', on='station_id')

# Week Data
to_merge = []
for station_id in df['station_id']:
    if np.isnan(station_id):
        print(f'Station id: {station_id} not found')
        continue
    df_main = pd.read_csv(f'station_summary/week_csv/week_{int(station_id)}.csv')
    df_main.drop(columns=df_main.columns[0], axis=1, inplace=True)
    df_main['date'] = df_main['date'].apply(lambda var: thai_datetime(var, day_data=False))
    df_main['station_id'] = int(station_id)
    to_merge += df_main.values.tolist()
df_to_merge = pd.DataFrame(to_merge, columns=['date', 'min_temp', 'max_temp', 'max_wind_dir',
                                              'max_wind_sp', 'rain_24h', 'note', 'station_id'])
df_week = df.merge(df_to_merge, how='left', on='station_id')

# Save to CSV files for later use
df.to_csv('assets/main_id_table.csv')
df_day.to_csv('assets/day_data.csv')
df_day.to_csv('assets/week_data.csv')