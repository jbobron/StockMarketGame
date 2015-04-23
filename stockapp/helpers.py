from models import db, User, Portfolio, StockHistory
from flask import session
import time
import apiRequests

def getArrayOfStocksFromPortfolio(query):
  stocks = []
  for row in query:
    x = str(row.ticker)
    stocks.append(x)
  return stocks


def getLastQueriedDateFromPortfolioForStock(stock):
  query = Portfolio.query.filter_by(email=session['email']).filter_by(ticker=stock).order_by(Portfolio.last_queried.desc())
  return query.first().last_queried

def getTodaysDate():
  return time.strftime('%Y-%m-%d')


def updateCurrentPricesAndLastQueriedDateOfThisStockInPortfolio(stock):
    #if last queried date in DB is Today
          #skip to next stock
    #else (last queried date for stock in DB is NOT today)
      #if there is NO last queried date for stock
            #make api call from execution date to today
            #update last queried date AND currentPrice for stock 
      #else (there is a last queried date for stock)
            #make api call from last queried date to today
            #update last queried date AND currentPrice for stock
    lastQueried = getLastQueriedDateFromPortfolioForStock(stock)
    todaysDate = getTodaysDate()
    if str(lastQueried) == todaysDate:   #if last queried date in DB is Today
      return    #skip to next stock
    else:
      if lastQueried == None:
        data = apiRequests.getToday(stock)
        for row in data:
          todaysPrice = row["Open"]
          break
        db.session.query(Portfolio).filter_by(ticker=stock).update({'last_queried': todaysDate})
        db.session.query(Portfolio).filter_by(ticker=stock).update({'currentPrice': todaysPrice})
        db.session.commit()



def updatePortfolioWorth(stocks):

  #from users grab portfolio worth
  query = db.session.query(User).filter_by(email=session['email'])
  portfolioWorth = query[0].portfolioWorth
  cashRemaining = query[0].cashRemaining
  #total
  total = 0.0
  #for each stock
  for stock in stocks:
    query = db.session.query(Portfolio).filter_by(email=session['email']).filter_by(ticker=stock)
    quantity = query[0].quantity
    currentPrice = query[0].currentPrice
    total = total + (quantity*currentPrice)
  portfolioWorth = total + cashRemaining
  print "PORTFOLIO WORTH:", portfolioWorth
  #portfolioWorth = total + RemainingCash
  db.session.query(User).filter_by(email=session['email']).update({'portfolioWorth': portfolioWorth})
  db.session.commit()






  # query = db.session.query(User).filter_by(email=session['email'])
  # for row in query:
  #   cashRemaining = row.cashRemaining
  #   portfolioWorth = row.portfolioWorth
  #   break
  # query = db.session.query(Portfolio).filter_by(email=session['email']).filter_by(ticker=stock)
  # for row in query:
  #   print "CurrentPrice : ", row.currentPrice
  #   print "price : ", row.price
  #   currentPrice = row.currentPrice
  #   break
  # # get stocks current price AND price(purchase price) from Portfolio table
  # # portfolioWorth = portfolioWorth + (currentPrice - purchasePrice)
  # portfolioWorth = cashRemaining + currentPrice
  # #worth = (quantity*currentPrice) + cash

  # # print "UPDATED PORTFOLIO WORTH ", portfolioWorth
  # db.session.query(User).filter_by(email=session['email']).update({'portfolioWorth': portfolioWorth})
  # db.session.commit()





