import pandas as pd
from bs4 import BeautifulSoup
import requests
"""
id_table columns:
id, province, station_id, station_name
"""
id_table = pd.read_csv('../assets/id_table.csv')
"""
True: If you want to scrap new daily (hourly) data but it will take time
False: Faster run for development purpose
scrape.py extract hourly data (update every 3 hours) of the last 24 hours only
Link to an example of a page the code scrapes: https://www.tmd.go.th/province_weather_stat.php?StationNumber=48455
"""
new_requests_station = True
# State Province id
for i, station_id in enumerate(id_table['station_id']):
    if new_requests_station:
        past_html = requests.get(f'https://www.tmd.go.th/province_weather_stat.php?StationNumber={station_id}')
        soup = BeautifulSoup(past_html.content, 'lxml')
    else:
        try:
            with open(f'station_html/{station_id}.html', 'rb') as f:
                soup = BeautifulSoup(f.read(), 'lxml')
        except:
            print(f'station id: {station_id} html has not downloaded')
            past_html = requests.get(f'https://www.tmd.go.th/province_weather_stat.php?StationNumber={station_id}')
            soup = BeautifulSoup(past_html.content, 'lxml')
            with open(f'station_html/{station_id}.html', 'wb+') as f:
                f.write(past_html.content)

    # Last 24 hours
    view0 = soup.find('div', id='view0')
    rows = view0.find_all('tr', align='center')
    row_list = []
    for row in rows:
        columns = row.find_all('td')
        column_list = []
        for column in columns:
            var = column.text.strip()
            column_list.append(var)
            if var == 'ลมสงบ':
                column_list.append(var)
        row_list.append(column_list)
    df = pd.DataFrame(row_list, columns=['datetime', 'temp', 'dew_point', 'rh',
                                         'pressure', 'wind_dir', 'wind_sp',
                                         'visibility', 'rain_3h', 'cloud'])

    # old_df = pd.read_csv(f'day_csv/day_{station_id}.csv')
    # new_df = pd.concat([old_df, df], join='inner')
    # new_df = new_df.drop_duplicates(subset=['datetime'], keep='last')
    df.to_csv(f'day_csv/day_{station_id}.csv')

    # Last 7 days
    view1 = soup.find('div', id='view1')
    rows = view1.find_all('tr', align='center')
    row_list = []
    for row in rows:
        columns = row.find_all('td')
        column_list = []
        for column in columns:
            var = column.text.strip()
            column_list.append(var)
            if var == 'ลมสงบ':
                column_list.append(var)
        row_list.append(column_list)
    df = pd.DataFrame(row_list, columns=['date', 'min_temp', 'max_temp', 'max_wind_dir',
                                         'max_wind_sp', 'rain_24h', 'note'])
    # old_df = pd.read_csv(f'week_csv/week_{station_id}.csv')
    # new_df = pd.concat([old_df, df], join='inner')
    # new_df = new_df.drop_duplicates(subset=['date'], keep='last')
    df.to_csv(f'week_csv/week_{station_id}.csv')

    print(station_id)
