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


def process_data(src, dist, src_traffic, dist_traffic):
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

    print('Filling missing numerical data...')
    # nadomestimo numericne podatke
    num_cols = df.select_dtypes(include=['number']).columns
    for col in num_cols:
        df[col].fillna((df[col].mean()), inplace=True)

    print('Transforming categorical data...')
    # kategoricni podatki
    df_location = pd.get_dummies(df['merilno_mesto'])
    df = pd.concat([df, df_location], axis=1).reindex(df.index)

    print('Dropping unuseful columns...')
    # neuporabni podatki
    df.pop('merilno_mesto')
    df.pop('sifra')
    df.pop('datum_od')
    df.pop('datum_do')

    stevilski = df[(["pm2.5", "nadm_visina", "o3", "benzen", "ge_sirina", "pm10", "co", "no2", "ge_dolzina", "so2"])]
    stevilski = stevilski.apply(pd.to_numeric, args=('coerce',))

    stevilski['pm2.5'].fillna(stevilski['pm2.5'].mean(), inplace=True)
    stevilski['nadm_visina'].fillna(stevilski['nadm_visina'].mean(), inplace=True)
    stevilski['o3'].fillna(stevilski['o3'].mean(), inplace=True)
    stevilski['benzen'].fillna(stevilski['benzen'].mean(), inplace=True)
    stevilski['ge_sirina'].fillna(stevilski['ge_sirina'].mean(), inplace=True)
    stevilski['pm10'].fillna(stevilski['pm10'].mean(), inplace=True)
    stevilski['co'].fillna(stevilski['co'].mean(), inplace=True)
    stevilski['no2'].fillna(stevilski['no2'].mean(), inplace=True)
    stevilski['ge_dolzina'].fillna(stevilski['ge_dolzina'].mean(), inplace=True)
    stevilski['so2'].fillna(stevilski['so2'].mean(), inplace=True)
    stevilski.isnull().sum()

    df_drop = df.drop(columns=stevilski)

    df = pd.concat([stevilski, df_drop], axis=1, join="inner")

    print('Saving processed data...')
    df.to_csv(dist, index=False)

    print('Finished air!')

    df_promet = pd.read_csv(src_traffic, sep = ";", decimal = ".", encoding = "cp1250")
    df_promet_filtered = df_promet[df_promet["Prometni odsek"].str.contains("CELJE|HRASTNIK|ISKRBA|KOPER|KRANJ|KRVAVEC|LJUBLJANA|BEŽIGRAD|CELOVŠKA|VIČ|MARIBOR|TITOVA|VRBANSKI|MURSKA SOBOTA|CANKARJEVA|RAKIČAN|NOVA GORICA|GRČNA|NOVO MESTO|OTLICA|PTUJ|REČICA|IL\.|TRBOVLJE|ZAGORJE")==True]
    df_promet_filtered = df_promet_filtered[['Prometni odsek', 'Vsa vozila (PLDP)']]

    df_promet_celje = df_promet_filtered[df_promet_filtered["Prometni odsek"].str.contains("CELJE")==True]
    df_promet_celje = df_promet_celje["Vsa vozila (PLDP)"].sum()
    
    df_promet_hrastnik = df_promet_filtered[df_promet_filtered["Prometni odsek"].str.contains("HRASTNIK")==True]
    df_promet_hrastnik = df_promet_hrastnik["Vsa vozila (PLDP)"].sum()
    
    df_promet_iskrba = df_promet_filtered[df_promet_filtered["Prometni odsek"].str.contains("ISKRBA")==True]
    df_promet_iskrba = df_promet_iskrba["Vsa vozila (PLDP)"].sum()
    
    df_promet_koper = df_promet_filtered[df_promet_filtered["Prometni odsek"].str.contains("KOPER")==True]
    df_promet_koper = df_promet_koper["Vsa vozila (PLDP)"].sum()
    
    df_promet_kranj = df_promet_filtered[df_promet_filtered["Prometni odsek"].str.contains("KRANJ")==True]
    df_promet_kranj = df_promet_kranj["Vsa vozila (PLDP)"].sum()
    
    df_promet_krvavec = df_promet_filtered[df_promet_filtered["Prometni odsek"].str.contains("KRVAVEC")==True]
    df_promet_krvavec = df_promet_krvavec["Vsa vozila (PLDP)"].sum()
    
    df_promet_jubljana = df_promet_filtered[df_promet_filtered["Prometni odsek"].str.contains("LJUBLJANA|BEŽIGRAD|CELOVŠKA|VIČ")==True]
    df_promet_jubljana = df_promet_jubljana["Vsa vozila (PLDP)"].sum()
    
    df_promet_maribor = df_promet_filtered[df_promet_filtered["Prometni odsek"].str.contains("MARIBOR|TITOVA|VRBANSKI")==True]
    df_promet_maribor = df_promet_maribor["Vsa vozila (PLDP)"].sum()
    
    df_promet_murska_sobota = df_promet_filtered[df_promet_filtered["Prometni odsek"].str.contains("MURSKA SOBOTA|CANKARJEVA|RAKIČAN")==True]
    df_promet_murska_sobota = df_promet_murska_sobota["Vsa vozila (PLDP)"].sum()
    
    df_promet_nova_gorica = df_promet_filtered[df_promet_filtered["Prometni odsek"].str.contains("NOVA GORICA|GRČNA")==True]
    df_promet_nova_gorica = df_promet_nova_gorica["Vsa vozila (PLDP)"].sum()
    
    df_promet_novo_mesto = df_promet_filtered[df_promet_filtered["Prometni odsek"].str.contains("NOVO MESTO")==True]
    df_promet_novo_mesto = df_promet_novo_mesto["Vsa vozila (PLDP)"].sum()
    
    df_promet_otlica = df_promet_filtered[df_promet_filtered["Prometni odsek"].str.contains("OTLICA")==True]
    df_promet_otlica = df_promet_otlica["Vsa vozila (PLDP)"].sum()
    
    df_promet_ptuj = df_promet_filtered[df_promet_filtered["Prometni odsek"].str.contains("PTUJ")==True]
    df_promet_ptuj = df_promet_ptuj["Vsa vozila (PLDP)"].sum()
    
    df_promet_il_bistrica = df_promet_filtered[df_promet_filtered["Prometni odsek"].str.contains("REČICA|IL\.")==True]
    df_promet_il_bistrica = df_promet_il_bistrica["Vsa vozila (PLDP)"].sum()
    
    df_promet_trbovlje = df_promet_filtered[df_promet_filtered["Prometni odsek"].str.contains("TRBOVLJE")==True]
    df_promet_trbovlje = df_promet_trbovlje["Vsa vozila (PLDP)"].sum()
    
    df_promet_zagorje = df_promet_filtered[df_promet_filtered["Prometni odsek"].str.contains("ZAGORJE")==True]
    df_promet_zagorje = df_promet_zagorje["Vsa vozila (PLDP)"].sum()

    df2 = df

    columns = ['pm2.5', 'nadm_visina', 'o3', 'benzen', 'ge_sirina', 'pm10', 'co',
       'no2', 'ge_dolzina', 'so2', 'CE Ljubljanska', 'CE bolnica', 'Hrastnik',
       'Iskrba', 'Koper', 'Kranj', 'Krvavec', 'LJ Bežigrad', 'LJ Celovška',
       'LJ Vič', 'MB Titova', 'MB Vrbanski', 'MS Cankarjeva', 'MS Rakičan',
       'NG Grčna', 'Novo mesto', 'Otlica', 'Ptuj', 'Rečica v I.Bistrici',
       'Trbovlje', 'Zagorje']

    df2 = df2.reindex(columns=columns)

    df2["promet"] = df2.apply(lambda row: df_promet_celje if row["CE Ljubljanska"] == 1
                          else df_promet_celje if row["CE bolnica"] == 1
                          else df_promet_hrastnik if row["Hrastnik"] == 1
                          else df_promet_iskrba if row["Iskrba"] == 1
                          else df_promet_koper if row["Koper"] == 1
                          else df_promet_kranj if row["Kranj"] == 1
                          else df_promet_krvavec if row["Krvavec"] == 1
                          else df_promet_jubljana if row["LJ Bežigrad"] == 1
                          else df_promet_jubljana if row["LJ Celovška"] == 1
                          else df_promet_jubljana if row["LJ Vič"] == 1
                          else df_promet_maribor if row["MB Titova"] == 1
                          else df_promet_maribor if row["MB Vrbanski"] == 1
                          else df_promet_murska_sobota if row["MS Cankarjeva"] == 1
                          else df_promet_murska_sobota if row["MS Rakičan"] == 1
                          else df_promet_nova_gorica if row["NG Grčna"] == 1
                          else df_promet_novo_mesto if row["Novo mesto"] == 1
                          else df_promet_otlica if row["Otlica"] == 1
                          else df_promet_ptuj if row["Ptuj"] == 1
                          else df_promet_il_bistrica if row["Rečica v I.Bistrici"] == 1
                          else df_promet_trbovlje if row["Trbovlje"] == 1
                          else df_promet_zagorje if row["Zagorje"] == 1
                          else None, axis=1)
    
    cat_cols_df2 = df2.select_dtypes(include=['object']).columns
    num_cols_df2 = df2.select_dtypes(include=['number']).columns

    for col in num_cols_df2:
        df2[col].fillna((df2[col].mean()), inplace=True)

    print('Saving processed traffic data...')
    df.to_csv(dist_traffic, index=False)

    print('Finished traffic!')


if __name__ == '__main__':

    root_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../..'))

    src_air = os.path.join(root_dir, 'data', 'raw', 'air')
    dist_air = os.path.join(root_dir, 'data', 'processed', 'processed_air')

    src_traffic = os.path.join(root_dir, 'data', 'raw', 'promet.csv')
    dist_traffic = os.path.join(root_dir, 'data', 'processed', 'processed_traffic')

    #src = os.path.join(root_dir, 'data', 'raw', 'data.json')
    #dist = os.path.join(root_dir, 'data', 'processed', 'data.csv')

    process_data(src_air, dist_air, src_traffic, dist_traffic)
