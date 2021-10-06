#importing libraries
import pandas as pd
import numpy as np
from IPython.display import display, HTML
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from collections import Counter
import seaborn as sns
from pymongo import MongoClient

# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = MongoClient(conn)

beer_df = pd.read_csv('beer_reviews (1).csv')
beer_df.head(-1)

beer_count=beer_df.groupby(['beer_beerid', 'beer_name']).count()['review_overall']
beer_count

beer_mean=beer_df.groupby(['beer_beerid', 'beer_name']).mean()
beer_mean

beer_overall = beer_mean.drop(columns=['brewery_id', 'review_time', 'beer_abv'])
beer_overall.insert('review_count', beer_count['review_overall'])

#shape of beer data
print("Number of reviews: ", beer_df.shape[0])
print("Number of features: ", beer_df.shape[1])
print("Total number of breweries; ", len(beer_df['brewery_name'].value_counts()))
print("Total number of beer style; ", len(beer_df['beer_style'].value_counts()))
print("Total number of beer names; ", len(beer_df['beer_name'].value_counts()))
print("Total number of brewery names; ", len(beer_df['brewery_name'].value_counts()))
print("Total number of brewery ID; ", len(beer_df['brewery_id'].value_counts()))


#find top 10 popular Breweries by review counts
popular_brewery = beer_df.groupby('brewery_name').brewery_name.count()
popular_brewery = popular_brewery.sort_values(ascending= False)
popular_breweries = popular_brewery.iloc[0:10]
popular_breweries

# top 10 beers with reviews count
top_100000_popular_beers = pd.DataFrame(beer_df.groupby('beer_name').beer_name.count().sort_values(ascending = False).iloc[0:100000])
top_100000_popular_beers.columns = ['Beer Names with Reviews counts']
top_100000_popular_beer

# top 10 beers with highest ratings
Top_beer_ratings = beer_df[['beer_name','review_overall']].groupby('beer_name').review_overall.agg('mean').sort_values(ascending = False)
Top_beer_ratings = Top_beer_ratings.iloc[0:10]
Top_beer_ratings.reset_index()

# missing data by rows
beer_row_clean = beer_df.dropna(subset=['brewery_id','brewery_name', 'beer_name', 'review_taste', 'review_overall', 'review_palate', 'review_aroma','beer_style', 'review_appearance'], how='any')
beer_row_clean.head(100000)

# brewery_df will have all the brewery information, specifically the id, and the brewery name.
brewery_df = beer_df[['brewery_id','brewery_name', 'beer_beerid', 'beer_name']].drop_duplicates(keep='first')
brewery_df1 = brewery_df.head(100000)
# convert brewery_df to the list of doctionary inorder to import them to MongoDB
table_1 = []

# import data to MongoDB
from pymongo import MongoClient
import json 
records= json.loads(brewery_df.to_json(orient='records'))

client = MongoClient()
client
client = MongoClient(host="localhost", port=27017)
db = client.BeerAdvocate_DB
collection = db.brewerydata

results = collection.insert_many(records)
results

# review_df will have all the various reviews for each of the beer id's or beer_beerid
review_df = beer_df[['beer_beerid', 'brewery_id','review_overall','review_aroma','review_appearance','review_palate','review_taste']].groupby('beer_beerid').mean().round(2)
review_df.reset_index()

# import data to MongoDB
from pymongo import MongoClient
import json 
records= json.loads(review_df.to_json(orient='records'))
# print (records)

client = MongoClient()
client
client = MongoClient(host="localhost", port=27017)
db = client.BeerAdvocate_DB
collection = db.reviewdata

results = collection.insert_many(records)
results

# beerid_df will have all the beer information such as name, style, and alcohol content for each beer_id
beerid_df = beer_df[['beer_beerid','beer_name','beer_style','beer_abv']].drop_duplicates('beer_beerid', keep='first').set_index('beer_beerid').sort_index()

# import data to MongoDB
from pymongo import MongoClient
import json 
records= json.loads(review_df.to_json(orient='records'))
# print (records)

client = MongoClient()
client
client = MongoClient(host="localhost", port=27017)
db = client.BeerAdvocate_DB
collection = db.beerdata

results = collection.insert_many(records)
results

#Which brewry produces the strongest beers by ABV%? (the mean of ABV for each brewry has beed considered due to the lenght of dataset)
data = beer_df.groupby('brewery_name').beer_abv.mean()
strong = pd.DataFrame(data.reset_index())

strong.columns = ['brewery_name', 'beer_abv_mean']

strongest = strong[strong.beer_abv_mean == strong.beer_abv_mean.max()]
strongest

#If asked pick the Top 3 beer consider following factors:
# 1)review_overall, 
# 2) review_aroma, 
# 3) review_appearance 
# 4) review_palate, 
# 5) review_taste
# 6) beer_abv

reviews = beer_df.groupby('beer_beerid').agg({'review_overall': np.mean,
                                'review_aroma': np.mean,
                                'review_appearance': np.mean,
                                'review_palate': np.mean,     
                                'review_taste': np.mean,
                                'beer_abv': np.mean})

picks = pd.DataFrame(reviews.reset_index())

finaltop = picks.sort_values(['review_overall', 'review_aroma','review_appearance','review_palate','review_taste','beer_abv'], ascending=[False,False, False, False, False, False])
finaltop[:5]

topbeers = finaltop.to_json()




