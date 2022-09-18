## Importing libraries

import pandas as pd 
import os
import matplotlib.pyplot as plt
import datetime

from itertools import combinations
from collections import Counter

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

## Task 4> Add City column using .apply()
def get_city(address):
    return address.split(',')[1]
def get_state(address):
    return address.split(',')[2].split(' ')[1]

all_data['City'] = all_data['Purchase Address'].apply(lambda x: f"{get_city(x)} ({get_state(x)})")
print(all_data.head())


## Question 1 - What was the best sales' month? How much was earned?
best_month = all_data.groupby('Month').sum()
# Shows sales bar chart per month
months = range(1,13)
plt.bar(months, best_month['Sales'])
plt.xticks(months)
plt.ylabel('Sales in US$')
plt.xlabel('Month')
print(plt.show())

## Question 2 - What city had the highest sales' number?
best_month = all_data.groupby('City').sum()
#Shows sales bar chart per city
cities = [city for city, df in all_data.groupby('City')]
plt.bar(cities, best_month['Sales'])
plt.xticks(cities, rotation='vertical', size=8)
plt.ylabel('Sales in US$')
plt.xlabel('City')
print(plt.show())

## Question 3 - What time should be displayed advertisements to max?
# Add Hour and Minute column
all_data['Order Date'] = pd.to_datetime(all_data['Order Date'])
all_data['Hour'] = all_data['Order Date'].dt.hour
all_data['Minute'] = all_data['Order Date'].dt.minute
print(all_data.head())
# Display sales rate bar chart per hour
hours = [hour for hour, df in all_data.groupby('Hour')]
plt.plot(hours, all_data.groupby(['Hour']).count())
plt.xticks(hours)
plt.xlabel('Hour')
plt.ylabel('Number of Orders')
plt.grid()
print(plt.show())

## Question 4 - What product are most often sold together?
df  = all_data[all_data['Order ID'].duplicated(keep=False)]
# Add Grouped sales column 
df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
df = df[['Order ID', 'Grouped']].drop_duplicates()
print(df.head())
# Counting unique pairs into a dict with itertools and collections libraries
# Refereced: https://stackoverflow.com/questions/53295887/counting-unique-pairs-of-numbers-into-a-python-dictionary

count = Counter()
# Creates a data frame with most commonly 'sold together' itens
for row in df['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list, 2)))
# Print data frame in rows
for key, value in count.most_common(10):
    print(key, value)

## Question 5 - What's the best-seller product?
product_group = all_data.groupby('Product')
qnt_ordered = product_group.sum()['Quantity Ordered']
# Plot best-seller items into bar chart
products = [product for product, df in product_group]
plt.bar(products, qnt_ordered)
plt.ylabel('Qnt')
plt.xlabel('Product')
plt.xticks(products, rotation='vertical', size=8)
print(plt.show())

# Arrange items per unitary price
prices = all_data.groupby('Product').mean()['Price Each']
# Plot second axis with line chart overlayered into bar chart
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.bar(products, qnt_ordered)
ax2.plot(products, prices, 'b-')

ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered', color='g')
ax1.set_xticklabels(products, rotation='vertical', size=8)
ax2.set_ylabel('Price US$', color='b')
print(plt.show())
