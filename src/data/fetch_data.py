import pandas as pd
import json
import os


def refactor_values(data):
    new_data = {}
    for key, value in data.items():
        if value != '':
            new_data[key] = value
        if isinstance(value, str) and '<' in value:
            new_value = value.split('<')[1]
            new_data[key] = int(new_value)
    return new_data


def process_data(src, dist):
    f = open(src, 'r', encoding='utf-8')
    raw = json.load(f)
    f.close()

    df = pd.DataFrame()

    print('Transforming json to pandas dataframe...')
    # prilagodimo json dataframe-u
    #for i in range(len(raw)):
    #    jdata = json.loads(raw[i]['json'])
    #    station = jdata['arsopodatki']['postaja']
    #    for i in range(len(station)):
    #        data = station[i]
    #        data = refactor_values(data)
    #        df = pd.concat([df, pd.json_normalize(data)])
    for i in range(len(raw)):
        data = raw[i]
        dictData = json.loads(data['json'])
    
    df1 = pd.json_normalize(dictData['arsopodatki']['postaja'])
    df = pd.concat([df, df1])#, axis=1, join="inner")

    df = df.reset_index(drop=True)    

    df_filtered = df.loc[df['merilno_mesto'] == 'MB Vrbanski'].copy()
    df_filtered['datum_od'] = pd.to_datetime(df_filtered['datum_od'], format='%Y-%m-%d %H')
    df_air = df_filtered[['datum_od', 'pm10']].copy()

    print('Saving processed air data...')
    df_air.to_csv(dist, index=False)

    print('Finished air!')



if __name__ == '__main__':

    root_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../..'))

    src = os.path.join(root_dir, 'data', 'raw', 'air')
    dist = os.path.join(root_dir, 'data', 'processed', 'processed_air')

    #src = os.path.join(root_dir, 'data', 'raw', 'data.json')
    #dist = os.path.join(root_dir, 'data', 'processed', 'data.csv')

    process_data(src, dist)
