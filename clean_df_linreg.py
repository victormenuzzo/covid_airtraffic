
# coding: utf-8

# In[4]:


import pandas as pd
import gc


# In[5]:


def split_date_columns(df):
    df['year'] = df['lastseen'].apply(lambda x: x[:4])
    df['month'] = df['lastseen'].apply(lambda x: x[5:7])
    df['day'] = df['lastseen'].apply(lambda x: x[8:10])
    df = df.drop(columns='lastseen')
    return df
def df_grouped(df):
    df = df.groupby(['pais_origem', 'pais_destino', 'year', 'month', 'day']).size().reset_index()
    df = pd.DataFrame(df)
    return df


# In[6]:


#2018
df = pd.read_csv('data/filghts_2018_limpo.csv')
df = split_date_columns(df)
df = df_grouped(df)

#2019 p1
df_2 = pd.read_csv('data/filghts_2019_1_limpo.csv')
df_2 = split_date_columns(df_2)
df_2 = df_grouped(df_2)
df = df.append(df_2)

#clean memory
del df_2
gc.collect()

#2019 p2
df_3 = pd.read_csv('data/filghts_2019_2_limpo.csv')
df_3 = split_date_columns(df_3)
df_3 = df_grouped(df_3)

#full dataframe
df = df.append(df_3)

#clean memory
del df_3
gc.collect()


# In[8]:


df.to_csv('data/df_linreg.csv', index=False)

