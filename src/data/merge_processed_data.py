import pandas as pd
import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data.preprocess_air_data import preprocess_air_data



def process_data(src_air, src_weather, dist):
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

    df_air = preprocess_air_data(df)

    print('Saving processed air data...')
    df_air.to_csv(dist, index=False)

    print('Finished air!')



if __name__ == '__main__':

    root_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../..'))
    

    src_air = os.path.join(root_dir, 'data', 'processed', 'data_air.csv')

    src_weather = os.path.join(root_dir, 'data', 'processed', 'processed_weather.csv')

    dist_merged = os.path.join(root_dir, 'data', 'processed', 'merged.csv')

    process_data(src_air, src_weather, dist_merged)
