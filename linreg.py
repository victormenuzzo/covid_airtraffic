from statsmodels.formula.api import ols
import pandas as pd
import datetime
import numpy as np

df = pd.read_csv('data/2018-2019linreg_allAircrafts.csv')

df['voos_soma_log'] = df["voos_soma"].apply(np.log)

model = ols("df.voos_soma_log ~ pais + valor_semana + dia_semana -1",  data=df)
response = model.fit()
response.summary()

###single test example
#ypred = response.predict({'pais':'Hong Kong', 'valor_semana': [2], 'dia_semana': [5]})
#print(np.expm1(ypred))

#this csv is obtained using prep_for_linreg file
df2020 = pd.read_csv('data/abr2020_realdata.csv')

def predict_values(x):
    return np.expm1(response.predict({'pais':x[0], 'valor_semana': x[1], 'dia_semana': x[2]}))

def pct_loss(x):
    return (x[4]-x[3])/x[4]

df2020['voos_pred'] = df2020.apply(predict_values, axis=1)
df2020['pct_loss'] = df2020.apply(pct_loss, axis=1)

df_pct_loss = df2020[['pais', 'pct_loss']].groupby('pais').mean().reset_index()
df_pct_loss.to_csv('data/flights_pct_loss.csv', index=False)

