import pandas as pd
from bs4 import BeautifulSoup
import requests
from station import *
import os

new_requests = False
new_requests_station = False
id_data = []
# State Province id
for i in range(81):
    province_id = i+1
    # Get HTML
    if new_requests:
        html = requests.get(f'https://www.tmd.go.th/province.php?id={province_id}')
        with open(f'html/{province_id}.html', 'wb+') as f:
            f.write(html.content)
        soup = BeautifulSoup(html.content, 'lxml')
    else:
        with open(f'html/{province_id}.html', 'rb') as f:
            soup = BeautifulSoup(f.read(), 'lxml')

    province_title = soup.find('span', class_='title').text.strip()
    '''
    Get station information
    '''
    station_list = []
    # Main Station
    try:
        st_html = soup.find('td', class_='SelectStation').a
        station_list.append(Station.from_datasource(st_html))
    except:
        print('Cannot scrape province id:', province_id)
        try:
            station_id = int(soup.find('td', class_='PLF').a['href'].split('=')[1])
            id_data.append([province_id, province_title, station_id, province_title])
        except:
            print(f'Province id: {province_id} has no station')
            continue
        continue

    # Other Stations
    other_st_html = soup.find_all('td', class_='UnselectStation')
    for st_html in other_st_html:
        station_list.append(Station.from_datasource(st_html.a))

    '''
    Get link to past information
    '''
    for station in station_list:
        print(station.name)
        print(station.id)
        new_row = [province_id, province_title, station.id, station.name]
        id_data.append(new_row)

        if new_requests_station:
            past_html = requests.get(f'https://www.tmd.go.th/province_weather_stat.php?StationNumber={station.id}')
            with open(f'station_html/{station.id}.html', 'wb+') as f:
                f.write(past_html.content)

# Create id table
id_table = pd.DataFrame(id_data, columns=['id', 'province', 'station_id', 'station_name'])
id_table = id_table.drop_duplicates(subset=['station_id'], keep='last').reset_index(drop=True)
id_table.to_csv('../assets/id_table.csv')
