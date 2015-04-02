import requests, pymongo, datetime, unicodedata
from pymongo import MongoClient


client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.test_database

collection = db.stockMarketGame

stockTickers = {'google':"GOOG", 'apple':"AAPL", 'facebook':"FB"} #4:"CSCO", 5:"YELP", 6:"LNKD", 7:"CRM", 8:"TSLA", 9:"XOM"


#https://api.mongodb.org/python/current/tutorial.html

def makeApiCallAndAddToMongo(collectionName, ticker):
  print collectionName
  client = MongoClient()
  client = MongoClient('localhost', 27017)
  db = client.test_database
  collection = db.stockMarketGame
  collectionName = db[collectionName]
  r = requests.get('https://www.quandl.com/api/v1/datasets/GOOG/NASDAQ_'+ticker+'.json?auth_token=W79xnmr9AzJZd5ZKw3gy')
  apiData = r.json()
  colNamesArr = []

  #gets column names into an array
  for x in apiData['column_names']:
    unUnicoded = unicodedata.normalize('NFKD', x).encode('ascii','ignore')
    colNamesArr.append(unUnicoded)

  # # create a object to send to mongoDB
  # # for each array in apiData data array
  # #   for the first element in each array
  # #     create a key value pair in mongoObj, the key being the first element in the subArr the value being an empty arr  

  for subArr in apiData['data']:
    count = 0
    currentObj = {}
    for element in subArr:
      print(currentObj)
      if count == 0:
        date = str(element)
        currentObj[colNamesArr[count]] = date
      else: 
        if(isinstance(element, float)):
          currentObj[colNamesArr[count]] = float(element)
      count = count + 1

    collectionName.insert(currentObj)
    print(collectionName.count())

for i in stockTickers:
  makeApiCallAndAddToMongo(i, stockTickers[i])




