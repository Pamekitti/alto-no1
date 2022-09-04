import pandas as pd
import numpy as np
from process_thai import thai_datetime


def get_day_data(df):
    to_merge = []
    for station_id in df['station_id']:
        if np.isnan(station_id):
            print(f'Station id: {station_id} not found')
            continue
        df_main = pd.read_csv(f'day_csv/day_{int(station_id)}.csv')
        df_main.drop(columns=df_main.columns[0], axis=1, inplace=True)
        df_main['datetime'] = df_main['datetime'].apply(lambda var: thai_datetime(var))
        df_main['station_id'] = int(station_id)
        to_merge += df_main.values.tolist()
    df_to_merge = pd.DataFrame(to_merge, columns=['datetime', 'temp', 'dew_point', 'rh',
                                                  'pressure', 'wind_dir', 'wind_sp',
                                                  'visibility', 'rain_3h', 'cloud', 'station_id'])
    df_day = df.merge(df_to_merge, how='left', on='station_id')

    return df_day


def get_week_data(df):
    to_merge = []
    for station_id in df['station_id']:
        if np.isnan(station_id):
            print(f'Station id: {station_id} not found')
            continue
        df_main = pd.read_csv(f'week_csv/week_{int(station_id)}.csv')
        df_main.drop(columns=df_main.columns[0], axis=1, inplace=True)
        df_main['date'] = df_main['date'].apply(lambda var: thai_datetime(var, day_data=False))
        df_main['station_id'] = int(station_id)
        to_merge += df_main.values.tolist()
    df_to_merge = pd.DataFrame(to_merge, columns=['date', 'min_temp', 'max_temp', 'max_wind_dir',
                                                  'max_wind_sp', 'rain_24h', 'note', 'station_id'])
    df_week = df.merge(df_to_merge, how='left', on='station_id')

    return df_week