
#%%
import pandas as pd
import numpy as np


#%%
playstoreDF = pd.read_csv('./datasets/googleplaystore.csv')


#%%
playstoreDF.columns

#%%
playstoreDF.shape

#%%
#Remove rows where Category = 1.9
playstoreDF = playstoreDF[playstoreDF['Category'] != '1.9']

#%%
playstoreDF.isnull().sum()

#%%
averagePerCategory = playstoreDF.groupby('Category')['Rating'].mean()
averagePerCategory['BEAUTY']

#%%
categories = averagePerCategory.index.values
for category in categories:
    #print(category)
    playstoreDF.loc[playstoreDF['Category'] == category, 'AverageCategoryRating'] = averagePerCategory[category] 
playstoreDF['AverageCategoryRating']

#%%
#Replacing NaN Ratings with average rating from that category
playstoreDF['Rating'].fillna(playstoreDF['AverageCategoryRating'],inplace = True)
playstoreDF['Rating'].isnull().sum()

#%%
#Drop other rows with NaN values and round of Ratings to one decimal point
playstoreDF.dropna(inplace=True)
playstoreDF.round(1)


#%%
#Converting the number of Installs to int64
playstoreDF['Installs'] = playstoreDF['Installs'].str[:-1]
playstoreDF['Installs'] = playstoreDF['Installs'].str.replace(',','')

#%%
playstoreDF['Installs'] = playstoreDF['Installs'].astype('int64')

#%%
#Clean up Size column
playstoreDF.loc[playstoreDF['Size'] == 'Varies with device'] = 0
playstoreDF['Size'] = playstoreDF['Size'].str.replace('M','e+6')
playstoreDF['Size'] = playstoreDF['Size'].str.replace('k','e+3')
playstoreDF['Size'].unique()

#%%
#Output to CSV
playstoreDF.to_csv('./datasets/cleanedPlayStore.csv', encoding = 'utf-8')

