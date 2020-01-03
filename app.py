import pymongo
import datetime
import json
import os
from flask import Flask, render_template, request, jsonify
from mongoengine import connect
from pymongo import *

## Author Christian Schuschnig

app = Flask(__name__)
try:
    client = pymongo.MongoClient(
        "mongodb+srv://christian:LkipSB6LPbBV8wM@mongodbmovie-702qa.mongodb.net/test?retryWrites=true&w=majority")
    db = client['masterproject']
    collection = db['survey']
    print("Connected to DB succesfully!")
except:
    print("Could not connect to MongoDB")


@app.route('/')
def index():
    ##return '<a href=' + url_for("hello", name="World") + '> Lass dich grüßen</a>'
    return render_template('home.html', thing_to_say='Click here to start')


@app.route('/poll.html')
def poll():
    ##return '<a href=' + url_for("hello", name="World") + '> Lass dich grüßen</a>'
    return render_template('poll.html', thing_to_say='Click here to start')


##@app.route("/db")
## def home_page():
##    online_users = mongo.db.users.find({"online": True})
##    return render_template("index.html",
##        online_users=online_users)


@app.route('/my_form', methods=['POST'])
def my_form():

    new = {
        "question1": str(request.form['question1']),
        "question2": str(request.form['question2']),
        "dropdown1": str(request.form['dropdown1']),
        "dropdown2": str(request.form['dropdown2']),
        "textbox": str(request.form['textbox']),
        "date": datetime.datetime.utcnow(),
    }

    try:
        _id = collection.insert_one(new)
        print("database entry successfully")
    except:
        print("database entry not successfully!")

    message = "db entry " + str(new) + " was successfully inserted in database"

    return str(message)


if __name__ == '__main__':
    app.run(debug=True)
