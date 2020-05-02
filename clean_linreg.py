
# coding: utf-8

# In[104]:


import pandas as pd
import datetime
import gc


# In[105]:


selected_aircrafts = ['ERJ 170-200 LR', 'BOEING 737-8AS', 'A320 214', '172S', 'A320-214', '737-7H4', 'A320-232', 'A320 232', 'A321-231', 'CL-600-2D24', '737-823', 'A320 214SL', '737-8H4', 'PA-28-181', '737-924ER', 'A321 231SL', 'AIRBUS A319-111', '737-800', 'A319 112', 'A321 231', 'CL-600-2B19', 'A320 232SL', 'A321-211', '172N', 'A319-112', 'A319 111', 'CL-600-2C10', '208B', 'EMB-145LR', 'AIRBUS A320-232', '737-824', '737NG 8FE/W', 'BD-100-1A10', 'SR22', '737NG 8K2/W', 'AIRBUS A320-214', '737NG 838/W', 'BOEING 737-800', '737-900ER', 'DHC-8-402 (Dehavilland)', 'AIRBUS A319-131', 'A330 343E', '172R', 'A319-132', '172M', '737NG 800/W', 'A380 861', 'SR20', '737NG 823/W', 'A319-111']
def get_models(df):
    return df[df.model.isin(selected_aircrafts)]

def add_dateinfo(df):
    df['lastseen'] = pd.to_datetime(df['lastseen'])
    df['valor_semana'] = df['lastseen'].apply(lambda x: x.isocalendar()[1])
    # 0 -> segunda .... 7 -> domingo
    df['dia_semana'] = df['lastseen'].apply(lambda x: x.weekday())
    return df


# In[106]:


#2018
df = pd.read_csv('data/filghts_2018_model.csv')
df  = get_models(df)
df = add_dateinfo(df)

#2019 p1
df_2 = pd.read_csv('data/filghts_2019_1_model.csv')
df_2  = get_models(df_2)
df_2 = add_dateinfo(df_2)
df = df.append(df_2)
#clean memory
del df_2
gc.collect()

#2019 p2
df_3 = pd.read_csv('data/filghts_2019_2_model.csv')
df_3  = get_models(df_3)
df_3 = add_dateinfo(df_3)
df = df.append(df_3)
#full dataframe
df = df.append(df_3)
#clean memory
del df_3
gc.collect()


# In[107]:


df_origem =df.groupby(['pais_origem', 'valor_semana', 'dia_semana']).size().reset_index()
df_origem = pd.DataFrame(df_origem)
df_origem.columns = ['pais', 'valor_semana','dia_semana', 'voos']

df_destino =df.groupby(['pais_destino', 'valor_semana', 'dia_semana']).size().reset_index()
df_destino = pd.DataFrame(df_destino)
df_destino.columns = ['pais', 'valor_semana','dia_semana', 'voos']

df_final = df_origem.merge(df_destino, 'outer', on = ['pais', 'valor_semana','dia_semana'])
df_final['voos_soma'] = df_final['voos_x'].fillna(0) + df_final['voos_y'].fillna(0)
lr = df_final[['pais','valor_semana','dia_semana','voos_soma']]
lr


# In[116]:


lr[lr.pais == 'Iran']


# In[108]:


from statsmodels.formula.api import ols

model = ols("voos_soma ~ pais + valor_semana + dia_semana",  data=lr)
response = model.fit()
response.summary()


# In[109]:


df_final.voos_soma.sum()

