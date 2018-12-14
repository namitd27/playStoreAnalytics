#%%
import pandas as pd
import numpy as np

#%%
psdf = pd.read_csv('./datasets/cleanedPlayStore.csv')

#%%
psdf.drop(psdf.columns[0], axis = 1)
psdf.round(1)

#%%
psdf['Installs'] = psdf['Installs'].str[:-1]
psdf['Installs'] = psdf['Installs'].str.replace(',','')
psdf['Installs'] = psdf['Installs'].astype('int64')

#%%
psdf['Installs'].describe()

#%%
#Which Category has the most installs?
categoryInstalls = psdf.groupby('Category')['Installs'].sum()
categoryInstalls.idxmax()