import datetime
import json
import random

import pymongo
from flask import Flask, render_template, request, url_for, redirect
from pymongo import *

## Author Christian Schuschnig

# Application contains global variables cause the split of the html files

## first decleration of global variables

# new variables for using arrays
title = []
description = []
trailer_link = []
genre = []

# write here how many movies should displayed at the page
pref_numMovies = 25
sugg_numMovies = 9

# variables for timestamps
date_page_task_description_1 = ''
date_page_pref_movie_2 = ''
date_page_rec_movie_3 = ''
date_page_questionnaire_4 = ''

# variables for rating the preference movies, for (Like/Dislike/unknown)
pre_movie_0 = "X"
pre_movie_1 = 'X'
pre_movie_2 = 'X'
pre_movie_3 = 'X'
pre_movie_4 = 'X'

pre_movie_0_title = "The Pianist"
pre_movie_0_description = "A Polish Jewish musician struggles to survive the destruction of the Warsaw ghetto of " \
                          "World War II. "
pre_movie_1_title = "Rataouille"
pre_movie_1_description = "A rat who can cook makes an unusual alliance with a young kitchen worker at a famous " \
                          "restaurant. "
pre_movie_2_title = "Inglorious Basterds"
pre_movie_2_description = "In Nazi-occupied France during World War II, a plan to assassinate Nazi leaders by a group " \
                          "of Jewish U.S. soldiers coincides with a theatre owner's vengeful plans for the same. "
pre_movie_3_title = "The Pianist"
pre_movie_3_description = "A Polish Jewish musician struggles to survive the destruction of the Warsaw ghetto of " \
                          "World War II. "
pre_movie_4_title = "No Country for Old Men"
pre_movie_4_description = "Violence and mayhem ensue after a hunter stumbles upon a drug deal gone wrong and more " \
                          "than two million dollars in cash near the Rio Grande. "
pre_movie_5_title = "Logan - The Wolverine"
pre_movie_5_description = "In a future where mutants are nearly extinct, an elderly and weary Logan leads a quiet " \
                          "life. But when Laura, a mutant child pursued by scientists, comes to him for help, " \
                          "he must get her to safety "
pre_movie_6_title = "The Bourne Ultimatum "
pre_movie_6_description = "Jason Bourne dodges a ruthless C.I.A. official and his Agents from a new assassination " \
                          "program while searching for the origins of his life as a trained killer.. "

# variables for rating the "suggested" movies, (Like/Dislike)
suggested_movie_1 = 'X'
suggested_movie_2 = 'X'
suggested_movie_3 = 'X'
suggested_movie_4 = 'X'
suggested_movie_5 = 'X'
suggested_movie_6 = 'X'
suggested_movie_7 = 'X'
suggested_movie_8 = 'X'
suggested_movie_9 = 'X'
suggested_movie_10 = 'X'

# variable for the "star" movie, gets the movie title
favourite = 'X'

# variables for questionnaire
poll_q1 = 'X'
poll_q2 = 'X'
poll_q3 = 'X'

# this variable is roundrobin princible, first user gets page 1, second user gets page 2, and so on
page = 1

app = Flask(__name__)

## Connection to the MongoDB Atlas Cloud

usr = 'christian'
pwd = 'LkipSB6LPbBV8wM'

try:
    client = pymongo.MongoClient(
        "mongodb+srv://" + usr + ":" + pwd + "@mongodbmovie-702qa.mongodb.net/test?retryWrites=true&w=majority")
    db = client['masterproject']
    # variable for writing poll data
    collection = db['survey']
    # variable for getting movie data
    collectíon_movies = db['movies']
    print("Connected to DB succesfully!")
except:
    print(
        "Could not connect to MongoDB. Write an E-Mail to chschusc@edu.aau.at with your IP-address to get access to the database")


@app.route('/get_survey')
# displays the data of the surveys collection
def get_surveys():
    documents = collection.find()
    response = []
    for document in documents:
        document['_id'] = str(document['_id'])
        response.append(document)
        response.append("<br/>")
    return json.dumps(response, indent=4, sort_keys=True, default=str)


@app.route('/get_movies')
# displays the data of the movies collection
def get_movies():
    documents = collectíon_movies.find()
    response = []
    for document in documents:
        document['_id'] = str(document['_id'])
        response.append(document)
    return json.dumps(response)


@app.route('/get_title')
def title():
    documents = str(collectíon_movies.find({"title": "Interstellar"}))
    return documents


@app.route('/home')
def index():
    ##return '<a href=' + url_for("hello", name="World") + '> Lass dich grüßen</a>'
    return render_template('home.html', thing_to_say='Click here to start')


@app.route('/poll.html')
##Routing to old poll, just for testing
def poll():
    ##return '<a href=' + url_for("hello", name="World") + '> Lass dich grüßen</a>'
    return render_template('poll.html', thing_to_say='Click here to start')


@app.route('/welcome.html')
def Movie_poll():
    ##return '<a href=' + url_for("hello", name="World") + '> Lass dich grüßen</a>'
    return render_template('/Movie-Poll.html', thing_to_say='Click here to start')


@app.route('/my_form', methods=['POST'])
##old poll app, just for testing things
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


@app.route('/')
def welcome():
    ##return '<a href=' + url_for("hello", name="World") + '> Lass dich grüßen</a>'
    return render_template('/welcome.html', thing_to_say='Click here to start')


@app.route('/task_description.html')
def task_description():
    ##return '<a href=' + url_for("hello", name="World") + '> Lass dich grüßen</a>'
    global date_page_task_description_1

    # timestamp
    date_page_task_description_1 = datetime.datetime.utcnow()

    return render_template('/task_description.html', thing_to_say='Click here to start')


@app.route('/pref_movies.html', methods=['POST', 'GET'])
def pref_movies():
    global pre_movie_0, pre_movie_1, pre_movie_2, pre_movie_3, pre_movie_4, date_page_pref_movie_2, page
    global pre_movie_0_description, pre_movie_0_title
    global pre_movie_1_description, pre_movie_1_title

    # timestamp
    date_page_pref_movie_2 = datetime.datetime.utcnow()

    ##pre_movie_0 = str(request.form.get('q4_overallSatisfaction[0]'))
    pre_movie_1 = str(request.form.get('q4_overallSatisfaction[1]'))
    pre_movie_2 = str(request.form.get('q4_overallSatisfaction[2]'))
    pre_movie_3 = str(request.form.get('q4_overallSatisfaction[3]'))
    pre_movie_4 = str(request.form.get('q4_overallSatisfaction[4]'))

    if request.method == 'POST':
        # will be exectued after form pref_movie_form is commited
        if page == 1:
            return redirect(url_for('rec_movies_1'))
        else:
            return redirect(url_for('rec_movies_2'))

    return render_template('/pref_movies.html', pre_movie_0_title=pre_movie_0_title, desc1=pre_movie_0_description)


@app.route('/rec_movies_1.html', methods=['POST', 'GET'])
def rec_movies_1():
    # list with 10 objects
    global suggested_movie_1, suggested_movie_2, suggested_movie_3, suggested_movie_4, suggested_movie_5, \
        suggested_movie_6, suggested_movie_7, suggested_movie_8, suggested_movie_9, suggested_movie_10, favourite, \
        date_page_rec_movie_3, page, sugg_numMovies

    dbmovies = db['movies']
    allsuggmovies = []

    name1 = dbmovies.find_one({'title': 'Interstellar'})

    # querying all titles
    # for x in range(0, sugg_numMovies):

    for movies in dbmovies.find({'type': 'rec'}, {"_id": False}):
        allsuggmovies.append(movies)

    # for randomizing the movie list
    random.shuffle(allsuggmovies)

    #for x in range(0, sugg_numMovies):
    #    titles.append() = allsuggmovies.split

    print(allsuggmovies)
    #print(allsuggmovies.pop())
    #
    # for x in range(0, sugg_numMovies):
    #    list = dbmovies.find()
    #    print('exit')

    date_page_rec_movie_3 = datetime.datetime.utcnow()

    suggested_movie_1 = str(request.form.get('q20_movies20[0]'))
    suggested_movie_2 = str(request.form.get('q20_movies20[1]'))
    suggested_movie_3 = str(request.form.get('q20_movies20[2]'))
    suggested_movie_4 = str(request.form.get('q20_movies20[3]'))
    suggested_movie_5 = str(request.form.get('q20_movies20[4]'))
    suggested_movie_6 = str(request.form.get('q20_movies20[5]'))
    suggested_movie_7 = str(request.form.get('q20_movies20[6]'))
    suggested_movie_8 = str(request.form.get('q20_movies20[7]'))
    suggested_movie_9 = str(request.form.get('q20_movies20[8]'))
    suggested_movie_10 = str(request.form.get('q20_movies20[9]'))

    favourite = str(request.form.get('q23_bestRecommended'))

    if request.method == 'POST':
        return redirect(url_for('questionnaire'))

    return render_template('/rec_movies_1.html', movie=allsuggmovies)


@app.route('/rec_movies_2.html', methods=['POST', 'GET'])
def rec_movies_2():
    # list with 10 objects + 2 additional objects
    global suggested_movie_1, suggested_movie_2, suggested_movie_3, suggested_movie_4, suggested_movie_5, \
        suggested_movie_6, suggested_movie_7, suggested_movie_8, suggested_movie_9, suggested_movie_10, favourite, \
        date_page_rec_movie_3, page

    date_page_rec_movie_3 = datetime.datetime.utcnow()

    suggested_movie_1 = str(request.form.get('q20_movies20[0]'))
    suggested_movie_2 = str(request.form.get('q20_movies20[1]'))
    suggested_movie_3 = str(request.form.get('q20_movies20[2]'))
    suggested_movie_4 = str(request.form.get('q20_movies20[3]'))
    suggested_movie_5 = str(request.form.get('q20_movies20[4]'))
    suggested_movie_6 = str(request.form.get('q20_movies20[5]'))
    suggested_movie_7 = str(request.form.get('q20_movies20[6]'))
    suggested_movie_8 = str(request.form.get('q20_movies20[7]'))
    suggested_movie_9 = str(request.form.get('q20_movies20[8]'))
    suggested_movie_10 = str(request.form.get('q20_movies20[9]'))

    favourite = str(request.form.get('q23_bestRecommended'))

    if request.method == 'POST':
        page = 1
        return redirect(url_for('questionnaire'))

    return render_template('/rec_movies_2.html', thing_to_say='Click here to start')


@app.route('/questionnaire.html', methods=['POST', 'GET'])
def questionnaire():
    global poll_q1, poll_q2, poll_q3, date_page_questionnaire_4

    date_page_rec_movie_4 = datetime.datetime.utcnow()

    poll_q1 = str(request.form.get('q26_theItems'))
    poll_q2 = str(request.form.get('q27_someOf'))
    poll_q3 = str(request.form.get('q28_theItems28'))

    if request.method == 'POST':
        return redirect(url_for('submit'))

    return render_template('/questionnaire.html', thing_to_say='Click here to start')


@app.route('/submit.html', methods=['POST', 'GET'])
def submit():
    return render_template('/submit.html', thing_to_say='Click here to start')


@app.route('/my_new_form', methods=['POST', 'GET'])
def my_new_form():
    ## Assignment of the resulted input of the html variables

    global page, pre_movie_0, pre_movie_1, pre_movie_2, pre_movie_3, pre_movie_4, suggested_movie_1, suggested_movie_2, \
        suggested_movie_3, suggested_movie_4, suggested_movie_5, suggested_movie_6, suggested_movie_7, suggested_movie_8, \
        suggested_movie_9, suggested_movie_10, poll_q1, poll_q2, poll_q3

    global date_page_task_description_1, date_page_pref_movie_2, date_page_rec_movie_3, date_page_questionnaire_4

    date_page_submit_5 = datetime.datetime.utcnow()

    ## saving in mongodb
    save(page, pre_movie_0, pre_movie_1, pre_movie_2, pre_movie_3, pre_movie_4, suggested_movie_1, suggested_movie_2,
         suggested_movie_3, suggested_movie_4, suggested_movie_5, suggested_movie_6, suggested_movie_7,
         suggested_movie_8, suggested_movie_9, suggested_movie_10, favourite, poll_q1, poll_q2, poll_q3,
         date_page_task_description_1, date_page_pref_movie_2, date_page_rec_movie_3, date_page_questionnaire_4,
         date_page_submit_5)

    # for the next user, so user 1 gets List 1, User 2 gets List 2, and so on
    if page == 1:
        page = 2
    else:
        page = 1

    return "Db entry successful"


def save(n, pre_movie_0_x, pre_movie_1_x, pre_movie_2_x, pre_movie_3_x, pre_movie_4_x, suggested_movie_1_x,
         suggested_movie_2_x, suggested_movie_3_x, suggested_movie_4_x, suggested_movie_5_x, suggested_movie_6_x,
         suggested_movie_7_x, suggested_movie_8_x, suggested_movie_9_x, suggested_movie_10_x,
         favourite_x, poll_q1_x, poll_q2_x, poll_q3_x, date_page_task_description_1_x,
         date_page_pref_movie_2_x, date_page_rec_movie_3_x, date_page_questionnaire_4_x,
         date_page_submit_5_x):
    """
    Saving in Cloud Atlas MongoDB
    """

    # variable n shows which page is used, if n is == 2 then user got list 2, is n == 1 then user got List 1

    new = {
        "Form": n,
        "pre_movie_0": pre_movie_0_x,
        "pre_movie_1": pre_movie_1_x,
        "pre_movie_2": pre_movie_2_x,
        "pre_movie_3": pre_movie_3_x,
        "pre_movie_4": pre_movie_4_x,
        "suggested_movie_1": suggested_movie_1_x,
        "suggested_movie_2": suggested_movie_2_x,
        "suggested_movie_3": suggested_movie_3_x,
        "suggested_movie_4": suggested_movie_4_x,
        "suggested_movie_5": suggested_movie_5_x,
        "suggested_movie_6": suggested_movie_6_x,
        "suggested_movie_7": suggested_movie_7_x,
        "suggested_movie_8": suggested_movie_8_x,
        "suggested_movie_9": suggested_movie_9_x,
        "suggested_movie_10": suggested_movie_10_x,
        "favourite": favourite_x,
        "poll_q1": poll_q1_x,
        "poll_q2": poll_q2_x,
        "poll_q3": poll_q3_x,
        "date_page_task_description_1": date_page_task_description_1_x,
        "date_page_pref_movie_2": date_page_pref_movie_2_x,
        "date_page_rec_movie_3": date_page_rec_movie_3_x,
        "date_page_questionnaire_4": date_page_questionnaire_4_x,
        "date_page_submit_5": date_page_submit_5_x,
    }
    try:
        ## Creates a new document in DB
        # creates a new ID for json-file in mongodb
        _id = collection.insert_one(new)
        print("database entry successfully")
    except:
        print("database entry not successfully!")
    # returns a successful message if sucessfull
    print("db entry " + str(new) + " was successfully inserted in database")
    ## return str(message)

    pass


def fill_datalist_pref():
    # for future to load datasets automatically in page
    pass


if __name__ == '__main__':
    app.run(debug=True)
