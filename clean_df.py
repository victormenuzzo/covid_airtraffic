import pandas as pd

def clean(df):
    df = df[['icao24','lastseen','departure', 'destination']]    
    df = df.dropna()
    return df

month_list = ['jan', 'fev', 'mar', 'abr', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']

for i in month_list:
    df_aux =  pd.read_csv('data/'+i+'2018.csv')
    df_aux = clean(df_aux)
    df = df.append(df_aux)
df.head()

#Loading aircraft model
aircraft = pd.read_csv('data/aircraftDatabase.csv')
aircraft = aircraft[['icao24', 'model']]
cods_aircraft = aircraft.icao24
aircraft = aircraft.set_index('icao24')
aircraft = aircraft.to_dict()

#Converting airport initials to country
airports = pd.read_csv('data/airports.csv')
airport_country = airports[['cod_icao', 'pais']]
cods_airports = airports.cod_icao
airport_country = airport_country.set_index('cod_icao')
airport_country = airport_country.to_dict()

#Adding origin country 
df['pais_origem'] = df['departure'].apply(lambda x: airport_country['pais'][x] if x in cods_airports.values else None)

#Adding destination country
df['pais_destino'] = df['destination'].apply(lambda x: airport_country['pais'][x] if x in cods_airports.values else None)

#Adding aircraft model
df['model'] = df['icao24'].apply(lambda x: aircraft['model'][x] if x in cods_aircraft.values else None)

df = df[['icao24','lastseen', 'pais_origem', 'pais_destino', 'model']]
df.to_csv('filghts_2018_model.csv', index=False)

