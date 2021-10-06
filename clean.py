import pandas as pd
import csv

def clean():
    dataframe = pd.DataFrame()
    clean_json = dataframe.to_json
    print('clean requested')
    return clean_json

# read the csv file
with open('beer_reviews.csv', mode = 'r') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        print(row)

# read the csv file as a dictionary
with open('beer_reviews.csv', mode = 'r') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    line_count=0
    for row in csvReader:
        if line_count==0:
            print(f'Column names are {",".join(row)}')
            
