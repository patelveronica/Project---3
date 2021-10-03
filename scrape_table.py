import pandas as pd
import numpy as np
from IPython.display import display, HTML
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from collections import Counter
import seaborn as sns
from pymongo import MongoClient

def table():
    conn = 'mongodb://localhost:27017'
    client = MongoClient(conn)
    beer_df = pd.read_csv('beer_reviews (1).csv')
    beer_df.head(-1)
    #shape of beer data
    print("Number of reviews: ", beer_df.shape[0])
    print("Number of features: ", beer_df.shape[1])
    print("Total number of breweries; ", len(beer_df['brewery_name'].value_counts()))
    print("Total number of beer style; ", len(beer_df['beer_style'].value_counts()))
    print("Total number of beer names; ", len(beer_df['beer_name'].value_counts()))
    print("Total number of brewery names; ", len(beer_df['brewery_name'].value_counts()))
    print("Total number of brewery ID; ", len(beer_df['brewery_id'].value_counts()))
    beer_row_clean = beer_df.dropna(subset=['brewery_id','brewery_name', 'beer_name', 'review_taste', 'review_overall', 'review_palate', 'review_aroma','beer_style', 'review_appearance'], how='any')
    beer_row_clean.head(800000)
    # Main Data Tables
    # brewery_df will have all the brewery information, specifically the id, and the brewery name.
    brewery_df = beer_df[['brewery_id','brewery_name']].drop_duplicates(keep='first')
    brewery_df1 = brewery_df.head(100000)
    # convert brewery_df to the list of doctionary inorder to import them to MongoDB
    table_1 = []
    from pymongo import MongoClient
    import json 
    records_brew= json.loads(brewery_df.to_json(orient='records'))

    client = MongoClient()
    client
    client = MongoClient(host="localhost", port=27017)
    db = client.BeerAdvocate_DB
    collection = db.brewerydata

    results_brew = collection.insert_many(records_brew)
    review_df = beer_df[['beer_beerid', 'brewery_id','review_overall','review_aroma','review_appearance','review_palate','review_taste']].groupby('beer_beerid').mean().round(2)
    review_df.reset_index()

    records= json.loads(review_df.to_json(orient='records'))
# print (records)
    client = MongoClient()
    client
    client = MongoClient(host="localhost", port=27017)
    db = client.BeerAdvocate_DB
    collection = db.beerdata

    results = collection.insert_many(records)
    data = beer_df.groupby('brewery_name').beer_abv.mean()
    strong = pd.DataFrame(data.reset_index())

    strong.columns = ['brewery_name', 'beer_abv_mean']

    strongest = strong[strong.beer_abv_mean == strong.beer_abv_mean.max()]
    reviews = beer_df.groupby('beer_beerid').agg({'review_overall': np.mean,
                                'review_aroma': np.mean,
                                'review_appearance': np.mean,
                                'review_palate': np.mean,     
                                'review_taste': np.mean,
                                'beer_abv': np.mean})

    picks = pd.DataFrame(reviews.reset_index())

    finaltop = picks.sort_values(['review_overall', 'review_aroma','review_appearance','review_palate','review_taste','beer_abv'], ascending=[False,False, False, False, False, False])
    return finaltop