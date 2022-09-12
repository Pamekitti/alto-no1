from data_processor.process_thai import thai_region
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import datetime as dt

# True if this is your first time, False for faster process
new_requests = True
station_frames = []
province_frames = []
# Get climate summary of all station in certain day
for dd_month in ['2022-07', '2022-08', '2022-09']:
    days_in_month = 31
    if dd_month == '2022-09':
        days_in_month = 11
    for day in range(days_in_month):
        dd_day = day + 1
        date = dt.datetime.strptime(f'{dd_month}-{dd_day}', '%Y-%m-%d')
        print(f'requesting {date} date')
        if new_requests:
            try:
                with open(f'responses/daily_{dd_month}_{dd_day}.html', 'rb') as f:
                    soup = BeautifulSoup(f.read(), 'lxml')
            except:
                url = "https://www.tmd.go.th/climate/climate.php?FileID=1"
                payload = {'ddlDay': str(dd_day),
                           'ddlMonth': dd_month}
                files = []
                headers = {}
                response = requests.request("POST", url, headers=headers, data=payload, files=files)
                soup = BeautifulSoup(response.content, 'lxml')
                with open(f'responses/daily_{dd_month}_{dd_day}.html', 'wb+') as f:
                    f.write(response.content)
        else:
            with open(f'responses/daily_{dd_month}_{dd_day}.html', 'rb') as f:
                soup = BeautifulSoup(f.read(), 'lxml')

        table = soup.find('table', border="1", bordercolor="#d9d9d9", bordercolordark="#ffffff",
                          bordercolorlight="#d9d9d9", cellpadding="3", cellspacing="0", width="100%")

        rows = table.find_all('tr', class_=['RDS', 'RADS', 'RH2'])
        region = 'north'
        data = []
        counter = 0
        for row in rows:
            if row['class'] == ['RH2']:
                region = thai_region(row.text.strip())
            else:
                row_list = [region]
                columns = row.find_all('td')
                # some station has no reported data on certain date
                if len(columns) == 8:
                    for i, value in enumerate(columns):
                        value = value.text.strip()
                        if value == 'ไม่มีฝน':
                            value = 0
                        if value == 'ฝนเล็กน้อย':
                            value = 0.1
                        row_list.append(value)
                elif len(columns) == 6:
                    for i, value in enumerate(columns):
                        if i == 3:
                            row_list += list(np.full(3, np.nan))
                        else:
                            value = value.text.strip()
                            if value == 'ไม่มีฝน':
                                value = 0
                            if value == 'ฝนเล็กน้อย':
                                value = 0.1
                            row_list.append(value)
                elif len(columns) == 2:
                    # append only the province name
                    row_list.append(columns[0].text.strip())
                    # add row full of nans
                    row_list += list(np.full(7, np.nan))
                else:
                    print(len(columns))
                    # append only the province name
                    row_list.append(columns[0].text.strip())
                    # add row full of nans
                    row_list += list(np.full(7, np.nan))
                data.append(row_list)

        # DataFrame from list of row_lists
        df = pd.DataFrame(data, columns=['region', 'station_name', 'max_temp', 'min_temp', 'wind_dir',
                                         'max_wind_v', 'time', 'rain_24h', 'yearly_rain'])
        df['date'] = date

        # Download id tables to map Thai station name to ids and english province names
        id_table = pd.read_csv('../assets/id_table.csv')
        main_id_table = pd.read_csv('../assets/main_id_table.csv')
        df = df.merge(id_table, how='right', on='station_name')

        # Create 1 file for all station
        df_station = df.merge(main_id_table[['eng_province', 'station_id']], how='left', on='station_id')
        # df_station.to_csv(f'station_summary/station_{dd_month}_{dd_day}.csv')
        station_frames.append(df_station)
        # Create 1 file for all province
        df_province = df.merge(main_id_table[['eng_province', 'station_id']], how='right', on='station_id')
        # df_province.to_csv(f'province_summary/province_{dd_month}_{dd_day}.csv')
        province_frames.append(df_province)

station_data = pd.concat(station_frames)
station_data = station_data.reset_index(drop=True)
station_data.to_csv('station_summary/station_all.csv')

province_data = pd.concat(province_frames)
province_data = province_data.reset_index(drop=True)
province_data.to_csv('province_summary/province_all.csv')




