import pandas as pd
from dateutil.relativedelta import relativedelta
pd.options.mode.chained_assignment = None  # default='warn'

# Map province name from Thai to English
def thai_province_map(id_main, json_map):
    eng_list = []
    for i in range(77):
        eng_list.append(json_map['features'][i]['properties']['name'])

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

    df = pd.DataFrame({'eng_province': eng_list})
    df = df.merge(mapper, how='left', on='eng_province')
    df = df.merge(id_main, how='left', on='province')

    return df

# Change thai month string to english
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
