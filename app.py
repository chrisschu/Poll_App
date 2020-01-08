import pymongo
import datetime
import json
import os
from flask import Flask, render_template, request, jsonify
from mongoengine import connect
from pymongo import *

##from flask_wtf import Form



##from flask_wtf import FlaskForm
##from datetime import date
##from wtforms.fields.html5 import DateField
##from wtforms.fields.html5 import DateTimeField

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


@app.route('/home')
def index():
    ##return '<a href=' + url_for("hello", name="World") + '> Lass dich grüßen</a>'
    return render_template('home.html', thing_to_say='Click here to start')


@app.route('/poll.html')
def poll():
    ##return '<a href=' + url_for("hello", name="World") + '> Lass dich grüßen</a>'
    return render_template('poll.html', thing_to_say='Click here to start')


@app.route('/')
def Movie_poll():
    ##return '<a href=' + url_for("hello", name="World") + '> Lass dich grüßen</a>'
    return render_template('/Movie-Poll.html', thing_to_say='Click here to start')


##@app.route("/db")
## def home_page():
##    online_users = mongo.db.users.find({"online": True})
##    return render_template("index.html",
##        online_users=online_users)


@app.route('/my_form', methods=['POST'])
def my_form():
    new = {
        "question1": str(request.form.get('question1')),
        "question2": str(request.form.get('question2')),
        "dropdown1": str(request.form.get('dropdown1')),
        "dropdown2": str(request.form.get('dropdown2')),
        "textbox": str(request.form.get('textbox')),
    }

    try:
        _id = collection.insert_one(new)
        print("database entry successfully")
    except:
        print("database entry not successfully!")

    message = "db entry " + str(new) + " was successfully inserted in database"

    return str(message)


@app.route('/my_new_form', methods=['POST', 'GET'])
def my_new_form():
    new = {
        "question1": str(request.form.get('q4_overallSatisfaction[0]')),
        "question2": str(request.form.get('q4_overallSatisfaction[1]')),
        "question1": str(request.form.get('q4_overallSatisfaction[0]')),
        "question2": str(request.form.get('q4_overallSatisfaction[1]')),
        "dropdown1": str(request.form.get('dropdown1')),
        "dropdown2": str(request.form.get('dropdown2')),
        "favouriteMovie": str(request.form.get('q23_bestRecommended')),
        "date_page_1": datetime.datetime.utcnow(),
        "date_page_2": datetime.datetime.utcnow(),
        "date_page_3": datetime.datetime.utcnow(),
        "date_page_4": datetime.datetime.utcnow(),
        "date_page_final": datetime.datetime.utcnow(),
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
