from stockapp import app
from flask import Flask
from flask import render_template, request, flash, session, url_for, redirect
from pymongo import Connection
import json
from bson import json_util
from bson.json_util import dumps
from models import db, User
from forms import ContactForm, SignupForm, SigninForm

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'test_database'
COLLECTION_NAME = 'apple' #CHANGE ME BASED ON WHAT DATA YOU WANT
FIELDS = {"Date":True, "Open":True, "High":True, "Low":True, "Close":True, "Volume":True}


@app.route("/")
def index():
  return render_template("index.html")

@app.route("/tempDashboard")
def dashBoard():
  return checkSessionBeforeRoutingTo("tempDashboard.html")

@app.route("/portfolio")
def portfolio():
    if 'email' not in session:
      return redirect(url_for('signin'))

    user = User.query.filter_by(email = session['email']).first()

    if user is None:
      return redirect(url_for('signin'))
    else:
      return render_template("portfolio.html")

@app.route("/rank")
def rank():
    return checkSessionBeforeRoutingTo("rank.html")

@app.route("/trade")
def trade():
    return checkSessionBeforeRoutingTo("trade.html")

@app.route('/testdb')
def testdb():
  if db.session.query("1").from_statement("SELECT 1").all():
    return 'It works.'
  else:
    return 'Something is broken.'

# @app.route("/ticker") #parse out additional endpoint to get tickr (ex:ticker/csco)
# def trade():
    #parse request info from client
    #make request to quandle
    #wait for response 
    #send info to client
    
# @app.route("/users/<int:userid>/") #parse out additional endpoint to get user (ex:user/andy)
# def capture_value_int(userid):
#     #hit mongoDB


@app.route("/googleStockData/projects")
def googleStockData_projects():
    connection = Connection(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME]
    projects = collection.find(fields=FIELDS)
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    connection.disconnect()
    return json_projects

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if 'email' in session:
      return redirect(url_for('profile'))

    if request.method == "POST":
      if form.validate() == False:
        return render_template("signup.html", form=form)
      else:
        newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
        db.session.add(newuser)
        db.session.commit() 

        session['email'] = newuser.email
        return redirect(url_for("portfolio"))

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
      return redirect(url_for('profile'))
                 
  elif request.method == 'GET':
    return render_template('signin.html', form=form)

@app.route('/signout')
def signout():
 
  if 'email' not in session:
    return redirect(url_for('signin'))
     
  session.pop('email', None)
  return redirect(url_for('index'))

def checkSessionBeforeRoutingTo(route):
  if 'email' not in session:
    return redirect(url_for('signin'))
  else:
    return render_template(route)



