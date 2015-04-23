import requests, pymongo, datetime, unicodedata
from pymongo import MongoClient

def getToday(ticker):
  ticker = ticker.upper()
  r = requests.get('https://www.quandl.com/api/v1/datasets/WIKI/'+ ticker +'.json?auth_token=ezzqdBWFN_Cm5xbN-sow?exclude_headers=true&rows=1')
  dirtyApiData = r.json()
  return cleanData(dirtyApiData)

def getHistory(ticker):
  ticker = ticker.upper()
  r = requests.get('https://www.quandl.com/api/v1/datasets/GOOG/NASDAQ_'+ticker+'.json?auth_token=ezzqdBWFN_Cm5xbN-sow')
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

def getDataSinceExecutionDate(executionDate, ticker):
  ticker = ticker.upper()
  r = requests.get('https://www.quandl.com/api/v1/datasets/WIKI/' + ticker + '.json?auth_token=ezzqdBWFN_Cm5xbN-sow?sort_order=asc&trim_start=' + executionDate)
  dirtyApiData = r.json()
  return cleanData(dirtyApiData)

def getDataSinceLastQuery(lastQueryDate, ticker):
  ticker = ticker.upper()
  r = requests.get('https://www.quandl.com/api/v1/datasets/WIKI/' + ticker + '.json?auth_token=ezzqdBWFN_Cm5xbN-sow?sort_order=asc&trim_start=' + lastQueryDate)
  dirtyApiData = r.json()
  return cleanData(dirtyApiData)



