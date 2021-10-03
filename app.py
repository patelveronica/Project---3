from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_table
import pandas as pd
import time

# create an instance of Flask
app = Flask(__name__)

# use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017")

import pymongo

# Rout to render index.html template using data from Mongo
@app.route("/")
def home():
    print("-----------------------------Home")
    beer_information = mongo.db.beerdata.find_one()
    return render_template("index.html", beer_information=beer_information)

# Rout that will trigger the scrape function
@app.route("/scrape")
def scrape():
    # run the scrape function
    beer_database = mongo.db.beerdata
    beer_information = scrape_table.scrape()
    # update the Mongo database using update and upsert=true
    beer_database.update({}, beer_information, upsert=True)
    return redirect('/')

# Redirect back to home page
    # return redirect("/")
if __name__ == "__main__":
    app.run(debug=True)
