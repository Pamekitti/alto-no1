import pandas as pd
from dateutil.relativedelta import relativedelta
pd.options.mode.chained_assignment = None  # default='warn'
import datetime as dt

# Map province name from Thai to English
def thai_province_map(id_main, json_map):
    """
    Map thai province name to English province, those exist in JSON Map

    Connecting data to location key in JSON allows us to visualize data in plotly choropleth.
    The function simply map using a table got from https://en.wikipedia.org/wiki/Provinces_of_Thailand
    which can map most of the provinces except some of these have to manually match below.

    Parameters
    ----------
    id_main: DataFrame
        DataFrame containing Thai province and ids that map to the weather data
    json_map: JSON file
        got from json.load("https://raw.githubusercontent.com/apisit/thailand.json/master/thailand.json")

    Returns
    -------
    df : DataFrame
        Mapped DataFrame
    """
    eng_list = []
    for i in range(77):
        eng_list.append(json_map['features'][i]['properties']['name'])

    name_map = pd.read_csv('assets/Provinces_of_Thailand_1.csv')
    print(name_map.columns)
    name_map[['province', 'eng_province']] = name_map[['Name\r\n(in Thai)', 'Namesake town/city']]
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

    df = pd.DataFrame({'eng_province': eng_list})
    df = df.merge(mapper, how='left', on='eng_province')
    df = df.merge(id_main, how='left', on='province')

    return df

# Change thai month string to english
def thai_datetime(test_str, day_data=True):
    '''
    Convert Thai month to numbers allow string to be converted to datetime later on
    The function inputs sting and outputs converted string
    '''
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

    if day_data:
        test_str = dt.datetime.strptime(test_str, '%d%m%y %H:%M') - relativedelta(years=43)
    else:
        test_str = dt.datetime.strptime(test_str, '%d%m%y') - relativedelta(years=43)
    return test_str

def thai_region(thai_str):
    '''
    Convert thai region names to English names
    '''
    eng_str = 'unknown_region'
    if thai_str == 'ภาคเหนือ':
        eng_str = 'north'
    if thai_str == 'ภาคตะวันออกเฉียงเหนือ':
        eng_str = 'north east'
    if thai_str == 'ภาคกลาง':
        eng_str = 'middle'
    if thai_str == 'ภาคตะวันออก':
        eng_str = 'east'
    if thai_str == 'ภาคใต้ (ฝั่งตะวันออก)':
        eng_str = 'west'
    if thai_str == 'ภาคใต้ (ฝั่งตะวันตก)':
        eng_str = 'south'
    return eng_str
