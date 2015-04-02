from flask import Flask
from flask import render_template
from pymongo import Connection
import json
from bson import json_util
from bson.json_util import dumps


app = Flask(__name__)


MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'test_database'
COLLECTION_NAME = 'apple' #CHANGE ME BASED ON WHAT DATA YOU WANT
FIELDS = {"Date":True, "Open":True, "High":True, "Low":True, "Close":True, "Volume":True}

# ROUTES IN PYTHON EXAMPLE: http://runnable.com/Uh4qRmSwz8cHAAAN/how-to-perform-advanced-routing-in-flask-for-python-and-routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tempDashboard")
def dashBoard():
    return render_template("tempDashboard.html")

@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")

@app.route("/rank")
def rank():
    return render_template("rank.html")

@app.route("/trade")
def trade():
    return render_template("trade.html")

# @app.route("/ticker") #parse out additional endpoint to get tickr (ex:ticker/csco)
# def trade():
#     #parse request info from client
#     #make request to quandle
#     #wait for response 
#     #send info to client
    
# @app.route("/user") #parse out additional endpoint to get user (ex:user/andy)
# def returnUserInfo():
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


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)