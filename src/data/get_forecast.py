import pandas as pd
import json
from urllib.request import urlopen
from datetime import datetime, timedelta

def get_forecast():
    url = "https://api.open-meteo.com/v1/forecast?latitude=46.5686&longitude=15.631&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"
    response = urlopen(url)
    data_json_forecast = json.loads(response.read())

    json_object_forecast = json.dumps(data_json_forecast)

    save_file = open("data/raw/forecast", "w")  
    json.dump(data_json_forecast, save_file)  
    save_file.close()  

    load_file = open('data/raw/forecast')
    dataJsonWeatherForecast = json.load(load_file)
    load_file.close()

    df_weather_forecast = pd.DataFrame.from_dict(json.loads(json.dumps(dataJsonWeatherForecast["hourly"])))

    df_weather_forecast['time'] = pd.to_datetime(df_weather_forecast['time'], format='%Y-%m-%d %H')

    #Pridobi trenutno uro in uro kasneje
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H")
    now = datetime.strptime(now_str, "%Y-%m-%d %H")
    print(now)
    hour = now + timedelta(hours=1)
    hour_str = hour.strftime("%Y-%m-%d %H")
    print(hour_str)

    df_forecast_filtered = df_weather_forecast.loc[df_weather_forecast['time'] == hour_str].copy()

    df_forecast = df_forecast_filtered.drop('time', axis=1)

    data_dict = df_forecast.to_dict(orient='records')[0]
    print("Finished")

    return data_dict