
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


def clean(df):
    df = df[['icao24','lastseen','departure', 'destination']]    
    df = df.dropna()
    return df

month_list = ['jan','fev', 'mar', 'abr', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
df = pd.DataFrame()
for i in month_list:
    df_aux =  pd.read_csv('data/'+i+'2018.csv')
    df_aux = clean(df_aux)
    df = df.append(df_aux)

df.head()


# In[4]:


aircraft = pd.read_csv('data/aircraftDatabase.csv')
aircraft = aircraft[['icao24', 'model']]

icao24_appe = df.icao24.unique()
cods_aircraft = aircraft.icao24
cods_aircraft_notin = list(set(icao24_appe) - set(cods_aircraft))
aircraft = aircraft.set_index('icao24')

aircraft = aircraft.to_dict()

airports = pd.read_csv('data/airports.csv')
airport_country = airports[['cod_icao', 'pais']]
cods_airports = airports.cod_icao
airport_country = airport_country.set_index('cod_icao')
#USAGE: airport_country['cod_icao']
airport_country = airport_country.to_dict()


df['model'] = df['icao24'].apply(lambda x: aircraft['model'][x] if x not in cods_aircraft_notin else None)

df['pais_destino'] = df['destination'].apply(lambda x: airport_country['pais'][x] if x in cods_airports.values else None)

df['pais_origem'] = df['departure'].apply(lambda x: airport_country['pais'][x] if x in cods_airports.values else None)


# In[5]:


df = df[['icao24','lastseen', 'pais_origem', 'pais_destino', 'model']]


# In[6]:


df.to_csv('filghts_2018_model.csv', index=False)

