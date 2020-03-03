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

# write here how many movies should displayed/used at the page
pref_numMovies = 50
sugg_numMovies = 10
quest_num = 5

# list for filling the survey data
preferred_movies = []
suggested_movies = []
questions = []
questions_rec = []
questions_pers = []

#
allprefmovies = []
allsuggmovies = []
allquestions_from_db_rec = []
allquestions_from_db_pers = []

# for the two movies likes of the user
user_likes_movies = []

# variables for timestamps
date_page_task_description_1 = ''
date_page_pref_movie_2 = ''
date_page_rec_movie_3 = ''
date_page_questionnaire_4 = ''

# list for all the movies in the watchlist
watchlist = []

# variable for the "star" movie, gets the movie title
favourite = 'X'

# variables for questionnaire
poll_q1 = 'X'
poll_q2 = 'X'
poll_q3 = 'X'

# roundrobin principle, first user gets page 1, second user gets page 2, and so on
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
    collection_movies = db['movies']
    collection_questions = db['questions']
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
    documents = collection_movies.find()
    response = []
    for document in documents:
        document['_id'] = str(document['_id'])
        response.append(document)
        response.append("<br/>")
        response.append("<br/>")
    return json.dumps(response)


@app.route('/drop_survey')
# planned feature to drop all data in database
def drop_survey():
    return "coming soon"


@app.route('/get_questions')
# planned feature to drop all data in database
def get_questions():
    documents = collection_questions.find()
    response = []
    for document in documents:
        document['_id'] = str(document['_id'])
        response.append(document)
        response.append("<br/>")
    return json.dumps(response, indent=4, sort_keys=True, default=str)


@app.route('/get_title')
def title():
    documents = str(collection_movies.find({"title": "Interstellar"}))
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


@app.route('/conditions.html')
def conditions():
    return render_template('/conditions.html', thing_to_say='Click here to start')


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


@app.route('/welcome.html')
def welcome():
    ##return '<a href=' + url_for("hello", name="World") + '> Lass dich grüßen</a>'
    return render_template('/welcome.html', thing_to_say='Click here to start')


@app.route('/')
def task_description():
    ##return '<a href=' + url_for("hello", name="World") + '> Lass dich grüßen</a>'
    global date_page_task_description_1

    # timestamp
    date_page_task_description_1 = datetime.datetime.utcnow()

    return render_template('/task_description.html', font_url='http://fonts.googleapis.com/css?family=PT+Sans:400,700')


@app.route('/pref_movies.html', methods=['POST', 'GET'])
def pref_movies():
    global date_page_pref_movie_2, page
    # for loading data into the HTML page (for example title, cover, stars ...)
    global allprefmovies
    # for getting the survey data (like/dislike/unknown)
    global preferred_movies
    # variable for generating the "you liked: " - feature
    global user_likes_movies

    # variable for storing 2 variable
    user_preferences = []

    allprefmovies.clear()
    preferred_movies.clear()

    dbmovies = db['movies']

    for movies in dbmovies.find({'type': 'pref'}, {"_id": False}):
        allprefmovies.append(movies)

    # for randomizing the movie list
    random.shuffle(allprefmovies)

    # print("allprefmovies: " + str(allprefmovies))
    # timestamp
    date_page_pref_movie_2 = datetime.datetime.utcnow()

    ##pre_movie_0 = str(request.form.get('q4_overallSatisfaction[0]'))
    # preferred_movies.append(str(request.form.get('q_pref_movies[1]')))

    if request.method == 'POST':
        # to get the html input, passed in this list variable
        for n in range(1, pref_numMovies):
            preferred_movies.append(str(request.form.get('q_pref_movies[' + str(n) + ']')))

        # print(len(preferred_movies))
        # print("pref_movies_first: n: " + str(preferred_movies))

        # variable geht die bewertete movieliste durch und speichert index/number in array.
        # this array will be used for displaying the movie in the next page
        for n in range(1, pref_numMovies - 1):
            if preferred_movies[n] == 'Like':
                # n + 1 generates the right "number" and fills user_preferences with two numbers
                user_preferences.append(n + 1)
                if len(user_preferences) == 2:
                    # if 2 likes found, end for loop
                    break

        user_likes_movies = []

        # movies = dbmovies
        # result = movies.find().limit(3)

        # loop is for filling user_likes_movies list, user preferences two
        try:
            for n in range(0, 2):
                print("user_preferences:" + str(user_preferences[n]))
                for movies in dbmovies.find({'number': user_preferences[n], 'type': "pref"}, {"_id": False}):
                    user_likes_movies.append(movies)
        except IndexError as error:
            print("Please Like 2 Movies")
    print("number 1: " + str(user_preferences))

    # for user_likes_movies in dbmovies.find
    # ({"$and": [{'type': 'pref'},{'number': int(user_preferences.pop)}], {"_id": False}):
    #    allprefmovies.append(user_likes_movies)

    # print("number 2: "+ str(user_preferences[1]))

    # for user_likes_movies in dbmovies.find({'type': 'pref'}, {'number': user_preferences.pop}, {"_id": False}):
    #   allprefmovies.append(user_likes_movies)

    # old data
    # pre_movie_1 = str(request.form.get('q4_overallSatisfaction[1]'))
    # pre_movie_2 = str(request.form.get('q4_overallSatisfaction[2]'))
    # pre_movie_3 = str(request.form.get('q4_overallSatisfaction[3]'))
    # pre_movie_4 = str(request.form.get('q4_overallSatisfaction[4]'))

    if request.method == 'POST':
        # will be exectued after form pref_movie_form is committed
        if page == 1:
            return redirect(url_for('rec_movies_1'))
        else:
            return redirect(url_for('rec_movies_2'))

    return render_template('/pref_movies.html', movie=allprefmovies)


@app.route('/rec_movies_1.html', methods=['POST', 'GET'])
def rec_movies_1():
    # list with 10 objects
    global favourite, date_page_rec_movie_3, page, sugg_numMovies, suggested_movies, allsuggmovies, watchlist
    global user_likes_movies, user_likes_movies, user_preferences
    print("allsugmovies: " + str(allsuggmovies))
    dbmovies = db['movies']

    allsuggmovies.clear()
    suggested_movies.clear()
    # just one query for testing, [deactivated]
    # name1 = dbmovies.find_one({'title': 'Interstellar'})

    # querying all titles
    # for x in range(0, sugg_numMovies):
    for movies in dbmovies.find({'type': 'rec'}, {"_id": False}):
        allsuggmovies.append(movies)

    # for randomizing the movie list
    random.shuffle(allsuggmovies)
    # for x in range(0, sugg_numMovies):
    #    titles.append() = allsuggmovies.split
    print("Länge" + str(len(allsuggmovies)))
    print("allsugmovies" + str(allsuggmovies))
    # print(allsuggmovies.pop())
    # suggested_movies = []
    # for x in range(0, sugg_numMovies):
    #    list = dbmovies.find()
    #    print('exit')
    date_page_rec_movie_3 = datetime.datetime.utcnow()

    if request.method == 'POST':
        for n in range(0, sugg_numMovies):
            suggested_movies.append(str(request.form.get('q20_movies20[' + str(n) + ']')))
        watchlist = request.form.getlist('q_Watchlist')
        favourite = str(request.form.get('q23_bestRecommended'))
    print("Watchlist:" + str(watchlist))

    if request.method == 'POST':
        return redirect(url_for('questionnaire'))
    print("User_likes_movies" + str(user_likes_movies))

    return render_template('/rec_movies_1.html', movie=allsuggmovies, user_pref=user_likes_movies)


@app.route('/rec_movies_2.html', methods=['POST', 'GET'])
def rec_movies_2():
    # list with 10 objects
    global favourite, date_page_rec_movie_3, page, sugg_numMovies, suggested_movies, allsuggmovies, watchlist
    global user_likes_movies, user_likes_movies, user_preferences

    dbmovies = db['movies']

    allsuggmovies.clear()
    suggested_movies.clear()
    # just one query for testing, [deactivated]
    # name1 = dbmovies.find_one({'title': 'Interstellar'})

    # querying all titles
    # for x in range(0, sugg_numMovies):
    for movies in dbmovies.find({'type': 'rec'}, {"_id": False}):
        allsuggmovies.append(movies)

    # for randomizing the movie list
    random.shuffle(allsuggmovies)
    # for x in range(0, sugg_numMovies):
    #    titles.append() = allsuggmovies.split
    print("Länge" + str(len(allsuggmovies)))
    print("allsugmovies" + str(allsuggmovies))
    # print(allsuggmovies.pop())
    # suggested_movies = []
    # for x in range(0, sugg_numMovies):
    #    list = dbmovies.find()
    #    print('exit')
    date_page_rec_movie_3 = datetime.datetime.utcnow()

    if request.method == 'POST':
        for n in range(0, sugg_numMovies):
            suggested_movies.append(str(request.form.get('q20_movies20[' + str(n) + ']')))
        watchlist = request.form.getlist('q_Watchlist')
        favourite = str(request.form.get('q23_bestRecommended'))
        print(suggested_movies)
    print("Watchlist:" + str(watchlist))

    if request.method == 'POST':
        return redirect(url_for('questionnaire'))
    print("User_likes_movies" + str(user_likes_movies))

    return render_template('/rec_movies_2.html', movie=allsuggmovies, user_pref=user_likes_movies)


@app.route('/questionnaire.html', methods=['POST', 'GET'])
def questionnaire():
    global poll_q1, poll_q2, poll_q3, date_page_questionnaire_4
    global questions, quest_num, questions_rec, questions_pers

    dbquestions = db['questions']

    questions_rec = []
    questions_pers = []
    print("questions_rec: " + str(questions_rec))
    print("questions_pers: " + str(questions_pers))
    # dbquestions = db['questions']

    allquestions_from_db_rec.clear()
    allquestions_from_db_pers.clear()

    # to get the questions about the recommended systems
    for questions_rec in dbquestions.find({'type': "rating_rec"}):
        allquestions_from_db_rec.append(questions_rec)

    # to get the questions about the personality
    for questions_pers in dbquestions.find({'type': "rating_pers"}):
        allquestions_from_db_pers.append(questions_pers)

    # to get the questions about the personality
    date_page_questionnaire_4 = datetime.datetime.utcnow()

    if request.method == 'POST':
        # to get the answered survey data about the personality
        # for n in range(0, len(allquestions_from_db_pers)): todo
            #questions_pers.append(str(request.form.get('q_survey_pers_' + str(n) + ']')))

        # to get the answered survey data about the recommended system
        #for n in range(0, len(allquestions_from_db_rec)): todo
            #questions_rec.append(str(request.form.get('q_survey_rec_' + str(n) + ']')))

        print("Länge" + str(len(allquestions_from_db_rec)))
        print("allquestions:" + str(allquestions_from_db_rec))

        print("all questions: " + str(allquestions_from_db_rec))

        print("questions_rec: " + str(questions_rec))
        print("questions_pers: " + str(questions_pers))
        return redirect(url_for('submit'))

    return render_template('/questionnaire.html', questions=allquestions_from_db_rec,
                           questions_pers=allquestions_from_db_pers)


@app.route('/submit.html', methods=['POST', 'GET'])
def submit():
    return render_template('/submit.html', thing_to_say='Click here to start')


@app.route('/my_new_form', methods=['POST', 'GET'])
def my_new_form():
    ## Assignment of the resulted input of the html variables

    global page, poll_q1, poll_q2, poll_q3, suggested_movies, sugg_numMovies, preferred_movies, pref_numMovies
    global date_page_task_description_1, date_page_pref_movie_2, date_page_rec_movie_3, date_page_questionnaire_4
    global watchlist, questions_rec, questions_pers

    date_page_submit_5 = datetime.datetime.utcnow()

    # print(preferred_movies)

    ## fuction for saving all data in mongo database
    save(suggested_movies, page, preferred_movies, favourite, watchlist,
         date_page_task_description_1, date_page_pref_movie_2, date_page_rec_movie_3, date_page_questionnaire_4,
         date_page_submit_5)

    # for the next user, so user 1 gets List 1, User 2 gets List 2, and so on
    if page == 1:
        page = 2
    else:
        page = 1

    return "Db entry successful"


def save(suggested_movies_x, page_x, preferred_movies_x,
         favourite_x, watchlist_x, date_page_task_description_1_x,
         date_page_pref_movie_2_x, date_page_rec_movie_3_x, date_page_questionnaire_4_x,
         date_page_submit_5_x):
    """
    Saving in Cloud Atlas MongoDB
    """

    # variable n shows which page is used, if n is == 2 then user got list 2, is n == 1 then user got List 1

    # idea is to merge to two lists to get one dictionary for inserting survey data in db

    # this list variable is for the left part of the dictionary (for example "pre_movie_0")
    pref_movie_attributename = []
    sugg_movie_attributename = []

    print("Watchlist!!!!!: " + str(watchlist))

    # https://docs.python.org/2/tutorial/datastructures.html#list-comprehensions
    for x in range(0, pref_numMovies):
        pref_movie_attributename.append('pref_movie_' + str(x))

    for x in range(0, sugg_numMovies):
        sugg_movie_attributename.append('sugg_movie_' + str(x))

    ##print("pref attribute name" + str(pref_movie_attributename)) TODO
    ##print("preferred movie x" + str(preferred_movies_x))

    # print(dict(zip(pref_movie_attributename, preferred_movies_x)))
    # print(dict(zip(sugg_movie_attributename, suggested_movies_x)))

    print("suggested movies" + str(suggested_movies))

    # using the dictionary form to input data in mongodb
    new = {
        "Form": page_x,
        "favourite": favourite_x,
        "date_page_task_description_1": date_page_task_description_1_x,
        "date_page_pref_movie_2": date_page_pref_movie_2_x,
        "date_page_rec_movie_3": date_page_rec_movie_3_x,
        "date_page_questionnaire_4": date_page_questionnaire_4_x,
        "date_page_submit_5": date_page_submit_5_x,
        "watchlist": watchlist_x
    }
    new.update(dict(zip(pref_movie_attributename, preferred_movies_x)))
    new.update(dict(zip(sugg_movie_attributename, suggested_movies_x)))
    # new.update(watchlist_x)

    try:
        ## Creates a new document in DB
        # creates a new ID for json-file in mongodb
        _id = collection.insert_one(new)
        print("database entry successfully")
    except:
        print("database entry not successfully!")
    # returns a successful message if successful
    print("db entry " + str(new) + " was successfully inserted in database")
    # print("to see output --> http://127.0.0.1:5000/get_survey")
    ## return str(message)

    pass


def fill_datalist_pref():
    # for future to load datasets automatically in page
    pass


if __name__ == '__main__':
    app.run(debug=True)
