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


    df_weather = pd.DataFrame.from_dict(json.loads(json.dumps(raw["hourly"])))
    df_weather['time'] = pd.to_datetime(df_weather['time'], format='%Y-%m-%d %H')

   

    print('Saving processed weather data...')
    df_weather.to_csv(dist, index=False)

    print('Finished weather!')



if __name__ == '__main__':

    root_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../..'))

    src = os.path.join(root_dir, 'data', 'raw', 'weather')
    dist = os.path.join(root_dir, 'data', 'processed', 'processed_weather')


    #src = os.path.join(root_dir, 'data', 'raw', 'data.json')
    #dist = os.path.join(root_dir, 'data', 'processed', 'data.csv')

    process_data(src, dist)
