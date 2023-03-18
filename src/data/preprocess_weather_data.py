import pandas as pd

def preprocess_weather_data(df_weather):
    
    df_weather['time'] = pd.to_datetime(df_weather['time'], format='%Y-%m-%d %H')

    return df_weather