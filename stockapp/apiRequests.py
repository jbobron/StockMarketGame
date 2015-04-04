import requests, pymongo, datetime, unicodedata
from pymongo import MongoClient

def makeApiCall(ticker):
  ticker = ticker.upper()
  r = requests.get('https://www.quandl.com/api/v1/datasets/GOOG/NASDAQ_'+ticker+'.json?auth_token=W79xnmr9AzJZd5ZKw3gy')
  dirtyApiData = r.json()
  return cleanData(dirtyApiData)

def cleanData(data):
  result = []
  colNamesArr = []
  for column in data['column_names']:
    unUnicoded = unicodedata.normalize('NFKD', column).encode('ascii','ignore')
    colNamesArr.append(unUnicoded)
  for subArr in data['data']:
    zeroIsForDates = 0
    currentObj = {}
    for element in subArr:
      if zeroIsForDates == 0:
        date = str(element)
        currentObj[colNamesArr[zeroIsForDates]] = date
      else:
        if(isinstance(element, float)):
          currentObj[colNamesArr[zeroIsForDates]] = float(element)
      zeroIsForDates = zeroIsForDates + 1
    result.append(currentObj)
  return result




