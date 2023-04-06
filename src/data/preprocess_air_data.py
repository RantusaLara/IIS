import pandas as pd

def preprocess_air_data(df):
    
    df_filtered = df.loc[df['merilno_mesto'] == 'MB Vrbanski'].copy()
    df_filtered['datum_od'] = pd.to_datetime(df_filtered['datum_od'], unit="s")
    df_air = df_filtered[['datum_od', 'pm10']].copy()


    return df_air