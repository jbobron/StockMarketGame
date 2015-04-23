from stockapp import app
from flask import Flask
from flask import render_template, request, flash, session, url_for, redirect
from pymongo import Connection
import json
from bson import json_util
from bson.json_util import dumps
from models import db, User, Portfolio, StockHistory
from forms import ContactForm, SignupForm, SigninForm, MakeTradeForm
import apiRequests
import sqlalchemy
import time
import helpers

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/portfolio")
def portfolio():
  user = User.query.filter_by(email=session['email']).first()
  if 'email' not in session:
    return redirect(url_for('signin'))
  if user is None:
    return redirect(url_for('signin'))
  user = User.query.filter_by(email=session['email']).first()
  portfolio = Portfolio.query.filter_by(email=session['email']).order_by(Portfolio.last_queried.desc())
  try:
    first = portfolio.first()
  except:
    first = None
  if first == None:
    return render_template("portfolio.html", user=user)
  stocks = helpers.getArrayOfStocksFromPortfolio(portfolio)
  for stock in stocks:
    helpers.updateCurrentPricesAndLastQueriedDateOfThisStockInPortfolio(stock)
  helpers.updatePortfolioWorth(stocks)
  return render_template("portfolio.html", user=user, portfolio=portfolio)

@app.route("/trade", methods=['GET','POST']) 
def reqForStock():
  form = MakeTradeForm()
  # if form.validate() == False:
    # return render_template("trade.html", form=form)
  if request.method == 'POST':
    ticker = str(form.ticker.data)
    quantity = int(form.quantity.data)
    data = apiRequests.getToday(ticker)[0]["Close"]
    total = quantity*data;
    # cashRemaining = total - cashRemaining;
    table = db.session.query(User)
    row = table.filter(User.email == session['email'])
    record = row.one()
    cash = record.cashRemaining
    if cash - total > 0:
      record.cashRemaining = cash - total
    else:
      return redirect(url_for('trade.html'))
    db.session.flush()
    print "STOCK PRICE", data
    newPort = Portfolio(session['email'], form.ticker.data, form.quantity.data, data, time.strftime('%Y/%m/%d'), None, data)
    # updateUser = update(User).where(session['email'] == User.email).values(cashRemaining=cashRemaining)
    db.session.add(newPort)
    db.session.commit() 
    return redirect(url_for('portfolio')) 
  # data = apiRequests.getHistory(ticker)
  if request.method == 'GET':
    return render_template("trade.html", form=form)

    
@app.route("/games", methods=['GET', 'POST'])
def game():
  form = MakeGameForm()
  return render_template("games.html", form=form)

@app.route("/rank")
def rank():
    return checkSessionBeforeRoutingTo("rank.html")

@app.route("/tempDashboard")
def dashBoard():
  return checkSessionBeforeRoutingTo("tempDashboard.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if 'email' in session:
      return redirect(url_for('profile'))

    if request.method == "POST":
      if form.validate() == False:
        return render_template("signup.html", form=form)
      else:
        initialCash = 1000000
        cashRemaining = 1000000
        newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data, initialCash, cashRemaining, cashRemaining)
        db.session.add(newuser)
        db.session.commit()

        session['email'] = newuser.email
        return redirect(url_for('portfolio')) 

        return "[1] Create a new user [2] sign in the user [3] redirect to the user's profile"
    
    elif request.method == "GET":
      return render_template("signup.html", form=form)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = SigninForm()
  
  if 'email' in session:
    return redirect(url_for('profile'))

  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signin.html', form=form)
    else:
      session['email'] = form.email.data
      return redirect(url_for('portfolio')) #TODO: Load current game before redirect
                 
  elif request.method == 'GET':
    return render_template('signin.html', form=form)

@app.route('/signout')
def signout():
 
  if 'email' not in session:
    return redirect(url_for('signin'))
     
  session.pop('email', None)
  return redirect(url_for('index'))

@app.route('/testdb')
def testdb():
  if db.session.query("1").from_statement("SELECT 1").all():
    return 'It works.'
  else:
    return 'Something is broken.'

def checkSessionBeforeRoutingTo(route):
  if 'email' not in session:
    return redirect(url_for('signin'))
  else:
    return render_template(route)



