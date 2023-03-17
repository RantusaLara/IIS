import pandas as pd
import json
import os



def process_data(src_air, src_weather, dist):

    df_air = pd.read_csv(src_air, sep = ",", decimal = ".")
    processed_weather = pd.read_csv(src_weather, sep = ",", decimal = ".")

    merged_df = pd.merge(df_air, processed_weather, left_on='datum_od', right_on='time', how='inner')
    merged_unique_df = merged_df.drop_duplicates()
    merged_unique_df = merged_unique_df.rename(columns={'datum_od': 'date'})

    koncni_df = merged_unique_df.drop(['time'], axis=1)

    koncni_df['temperature_2m'].fillna(koncni_df['temperature_2m'].mean(), inplace=True)
    koncni_df['relativehumidity_2m'].fillna(koncni_df['relativehumidity_2m'].mean(), inplace=True)
    koncni_df['windspeed_10m'].fillna(koncni_df['windspeed_10m'].mean(), inplace=True)

    stevilski = koncni_df[(["pm10"])]
    stevilski = stevilski.apply(pd.to_numeric, args=('coerce',))
    stevilski['pm10'].fillna(stevilski['pm10'].mean(), inplace=True)

    df_drop = koncni_df.drop(columns=stevilski)
    koncni_df = pd.concat([stevilski, df_drop], axis=1, join="inner")
   

    print('Saving merged data...')
    koncni_df.to_csv(dist, index=False)

    print('Finished merged!')



if __name__ == '__main__':

    root_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../..'))

    src_air = os.path.join(root_dir, 'data', 'processed', 'data_air.csv')

    src_weather = os.path.join(root_dir, 'data', 'processed', 'processed_weather.csv')

    dist_merged = os.path.join(root_dir, 'data', 'processed', 'merged.csv')

    process_data(src_air, src_weather, dist_merged)
