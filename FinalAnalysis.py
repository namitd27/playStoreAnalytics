
#%%
import pandas as pd
import numpy as np


#%%
playstoreDF = pd.read_csv('googleplaystore.csv')


#%%
playstoreDF.columns

#%%
playstoreDF.shape

#%%[markdown]
# Removing Category = 1.9

#%%
playstoreDF = playstoreDF[playstoreDF['Category'] != '1.9']
playstoreDF = playstoreDF[playstoreDF['Category'] != '0']

#%%[markdown]
# Replacing the NaN values in Rating with Average Rating for the corresponding Category

#%%
averagePerCategory = playstoreDF.groupby('Category')['Rating'].mean()

#%%
#Getting average per category
categories = averagePerCategory.index.values
for category in categories:
    #print(category)
    playstoreDF.loc[playstoreDF['Category'] == category, 'AverageCategoryRating'] = averagePerCategory[category] 
playstoreDF['AverageCategoryRating']

#%%
#Replacing NaN Ratings with average rating from that category
playstoreDF['Rating'].fillna(playstoreDF['AverageCategoryRating'],inplace = True)
playstoreDF['Rating'].isnull().sum()


#%% [markdown]
#Drop other rows with NaN values and round of Ratings to one decimal point

#%%
playstoreDF.dropna(inplace=True)
playstoreDF.round(1)


#%% [markdown]
#Converting the number of Installs to int64

#%%
playstoreDF['Installs'] = playstoreDF['Installs'].str[:-1]
playstoreDF['Installs'] = playstoreDF['Installs'].str.replace(',','')
playstoreDF['Installs'] = playstoreDF['Installs'].astype(np.int64)

#%%[markdown]
#Clean up Size column
#Convert to KiloByte and Column Type to float64

#%%
playstoreDF.loc[playstoreDF['Size'] == "Varies with device"] = '0'
playstoreDF['Size'] = playstoreDF['Size'].str.replace('M','000')
playstoreDF['Size'] = playstoreDF['Size'].str.replace('.','')
playstoreDF['Size'] = playstoreDF['Size'].str.replace('k','')
playstoreDF['Size'] = playstoreDF['Size'].astype('float64')
playstoreDF['Size']


#%% [markdown]
#Removing $ from the Price column and converting to float64

#%%
playstoreDF['Price'] = playstoreDF['Price'].str.replace('$', '')
playstoreDF['Price'] = playstoreDF['Price'].astype('float64')


#%% [markdown]
#Working on the Reviews Column

#%%
playstoreDF['Reviews'] = playstoreDF['Reviews'].astype('int64')

#%% [markdown]
# Using the formula below to get final rating
# FinalRating = (P*Rating) + 5*(1 - P)*(1-e^(-1*Reviews/Q))
# Where P, Q are weights to Rating and Reviews respectively and 0 < P < 1
# The choice of Q depends on what you call "few", "moderate", "many". 
# As a rule of thumb consider a value M that you consider "moderate" and take Q=−M/ln(1/2)≈1.44M.
# So if you think 100 is a moderate value the take Q=144. 
# Source: https://math.stackexchange.com/questions/942738/algorithm-to-calculate-rating-based-on-multiple-reviews-using-both-review-score


#%%
P = 0.5
Q = 144
reviewQuality = np.exp(-1 * playstoreDF['Reviews'].astype(float) / Q)
playstoreDF['FinalRating'] = (P * playstoreDF['Rating'].astype(np.float64)) + (5 * (1 - P) * (1 - reviewQuality))


#%%
playstoreDF['FinalRating'].describe()


#%% [markdown]
# We now have a clean dataframe to work with. <br>
# Our first requirement is to identify the Category with most Installs

#%%
#Which Category has the most Installs on an aveerage?
playstoreDF.groupby('Category')['Installs'].sum().astype(float).idxmax()

#%% [markdown]
# Our second requirement is to get Top Rated App in each Category


#%%
maxByCategory = playstoreDF.groupby('Category')['FinalRating'].idxmax()
playstoreDF[playstoreDF.index.isin(maxByCategory.values)][['App', 'Category', 'FinalRating']]


#%%[markdown]
# How many apps in each price bucket?


#%%[markdown]
# Creating buckets for Price Range
# Free - 0.0
# 1 => 0.0 - 1.0; 2=>1.0-10.0 and so on..

#%%
priceBins = [0, 1, 10, 50, 100, 200, 400]
labels = [1,2,3,4,5,6]
playstoreDF['PriceBuckets'] = pd.cut(playstoreDF['Price'], bins = priceBins, labels = labels)
playstoreDF['PriceBuckets'] = playstoreDF['PriceBuckets'].cat.add_categories(0.0).fillna(0.0)
playstoreDF[playstoreDF['Price'] > 0]


#%%
playstoreDF.groupby('PriceBuckets')['App'].count()

#%%[markdown]
# How many app installs on an average in each price bucket?

#%%
playstoreDF['Installs'] = playstoreDF['Installs'].astype(np.int64)
playstoreDF.groupby('PriceBuckets')['Installs'].mean()


#%%[markdown]
# Which are the top rated apps in each price bucket?

#%%
topPerBucket = playstoreDF.groupby('PriceBuckets')['FinalRating'].idxmax()
playstoreDF[playstoreDF.index.isin(topPerBucket.values)][['App','PriceBuckets','FinalRating']].sort_values(by=['PriceBuckets'])