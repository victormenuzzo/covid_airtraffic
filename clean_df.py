
# coding: utf-8

# In[1]:


import pandas as pd


# In[13]:


def clean(df):
    df = df[['lastseen','departure', 'destination']]
    df = df.dropna()
    return df

jan = pd.read_csv('data/jan2018.csv')
df = clean(jan)


month_list = ['fev', 'mar', 'abr', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']

for i in month_list:
    df_aux =  pd.read_csv('data/'+i+'2018.csv')
    df_aux = clean(df_aux)
    df = df.append(df_aux)
df.head()


# In[43]:


airports = pd.read_csv('data/airports.csv')
airport_country = airports[['cod_icao', 'pais']]
cods = airports.cod_icao
airport_country = airport_country.set_index('cod_icao')

#USAGE: airport_country['cod_icao']
airport_country = airport_country.to_dict()
df['pais_origem'] = 0
df['pais_origem'] = df['departure'].apply(lambda x: airport_country['pais'][x] if x in cods.values else None)

df['pais_destino'] = 0
df['pais_destino'] = df['destination'].apply(lambda x: airport_country['pais'][x] if x in cods.values else None)


# In[46]:


df = df[['lastseen', 'pais_origem', 'pais_destino']]


# In[47]:


df.to_csv('filghts_2018_limpo.csv', index=False)

