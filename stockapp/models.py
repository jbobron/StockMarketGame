from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
import datetime

db = SQLAlchemy()

class User(db.Model):
  __tablename__ = 'users'
  uid = db.Column(db.Integer, primary_key = True)
  firstname = db.Column(db.String(100))
  lastname = db.Column(db.String(100))
  email = db.Column(db.String(120), unique=True)
  pwdhash = db.Column(db.String(54))
  initialCash = db.Column(db.Float)
  cashRemaining = db.Column(db.Float)
  portfolioWorth = db.Column(db.Float)

  def __init__(self, firstname, lastname, email, password, initialCash, cashRemaining, portfolioWorth):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.email = email.lower()
    self.set_password(password)
    self.initialCash = initialCash
    self.cashRemaining = cashRemaining
    self.portfolioWorth = portfolioWorth

  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)



# class Portfolio(db.Model):
#   __tablename__ = 'portfolio'
#   pid = db.Column(db.Integer, primary_key = True)
#   stock_id = db.Column(db.Integer, db.ForeignKey('stock.sid'))
#   u_id = db.Column(db.Integer, db.ForeignKey('users.uid'))
#   g_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
#   executionDate = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class Stock(db.Model):
  __tablename__ = 'stock'
  sid = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(100))
  symbol = db.Column(db.String(8))
  # portfolios = db.relationship("Portfolio", backref="stock")


class Group(db.Model):
  __tablename__ = "groups"
  gid = db.Column(db.Integer, primary_key = True)
  groupname = db.Column(db.String(100))
  startDate = db.Column(db.DateTime)
  endDate = db.Column(db.DateTime)
  cash = db.Column(db.Float)

class UserGroups(db.Model):
  __tablename__ = "userGroups"
  ugid = db.Column(db.Integer, primary_key = True)
  u_id = db.Column(db.Integer, db.ForeignKey('users.uid'))
  g_id = db.Column(db.Integer, db.ForeignKey('groups.id'))


class Portfolio(db.Model):
  __tablename__ = 'portfolio'
  pid = db.Column(db.Integer, primary_key = True)
  email = db.Column(db.String(100))
  ticker = db.Column(db.String(100))
  quantity = db.Column(db.Integer)
  price = db.Column(db.Float)
  execution_date = db.Column(db.String(100))
  last_queried = db.Column(db.String(100))
  currentPrice = db.Column(db.Float)

  def __init__(self, email, ticker, quantity, price, execution_date, last_queried, currentPrice):
    self.email = email.title()
    self.ticker = ticker.title()
    self.quantity = quantity.title()
    self.price = price
    self.execution_date = execution_date
    self.last_queried = last_queried
    self.currentPrice = currentPrice


class StockHistory(db.Model):
  __tablename__ = 'stockshistory'
  id = db.Column(db.Integer, primary_key = True)
  Ticker = db.Column(db.String(100))
  Volume = db.Column(db.Float)
  High = db.Column(db.Float)
  Low = db.Column(db.Float)
  Date = db.Column(db.String(100))
  Close = db.Column(db.Float)
  Open = db.Column(db.Float)

  def __init__(self, Ticker, Volume, High, Low, Date, Close, Open):
    self.Ticker = Ticker
    self.Volume = Volume
    self.High = High
    self.Low = Low
    self.Date = Date
    self.Close = Close
    self.Open = Open
