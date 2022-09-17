## Importing libraries

import pandas as pd 
import os
import matplotlib as plt

## Task 1> Merging the files of Sales_Data into a single CSV file named full_sales.csv

files = [file for file in os.listdir('./Sales_Data/')]
full_data = pd.DataFrame()

for file in files:
    data_frame = pd.read_csv("./Sales_Data/"+file)
    full_data = pd.concat([full_data, data_frame])

full_data.to_csv("full_data.csv", index=False)

## Read full updated data frame and store in all_data

all_data = pd.read_csv("full_data.csv")
print(all_data.head())

## Clean up!!! Taking off NaN cells

nan_df = all_data[all_data.isna().any(axis=1)]
print(nan_df.head())
all_data = all_data.dropna(how='all')
print(all_data.head())

## Find 'Or' and fix it

all_data = all_data[all_data['Order Date'].str[0:2] != 'Or']

## Convert columns values to correct type
## Make integer
all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
## Make float
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])

## Augment data with additional columns

## Task 2> Add Month column

all_data['Month'] = all_data['Order Date'].str[0:2]
all_data['Month'] = all_data['Month'].astype('int32')
print(all_data.head())


## Task 3> Add Sales column

all_data['Sales'] = all_data['Quantity Ordered'] * all_data['Price Each']
print(all_data.head())

## Question 1 - What was the best sales' month? How much was earned?
best_month = all_data.groupby('Month').sum()
# Shows month with higher sales value
print(best_month['Sales'].nlargest(n=1))