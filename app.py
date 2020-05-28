import datetime
import json
import random

import pandas as pd
import pymongo
from flask import Flask, render_template, request, url_for, redirect, session, flash
from pymongo import *

## Author Christian Schuschnig

## first decleration of global variables

# application works with global variables
# these global variables serves as cache, data will be transfered  to sessions to get no parallel conflict


# list for filling the survey data
# these variable lists will be first fullfilled, then the session variables
likes_list = []
dislikes_list = []
neutral_list = []
preferred_movies = []
questionnaire_answer_from_survey = []
questionnaire_answer_from_survey_pers = []
questions_rec = []
questions_pers = []

# global variable list for getting the fill the html page
allprefmovies = []
allsuggmovies = []
allquestions_from_db_rec = []
allquestions_from_db_pers = []

# for checking shuffling after fillin html page
check_shuffling = 0

# for the two movies likes of the user
user_likes_movies = []

# variables for timestamps
date_page_task_description_1 = ''
date_page_pref_movie_2 = ''
date_page_rec_movie_3 = ''
date_page_questionnaire_4 = ''

# list for all the movies in the watchlist
watchlist = []

# declaration boolean variable for fake, if in like_list/dislike_list Movie Popeye (number , defined as number
# in mongo db1)
# is contained --> fake = true
fake = False

app = Flask(__name__)

# secret key for using the flask session
app.config['SECRET_KEY'] = 'testkgdfsgdwrey'

## Connection to the MongoDB Atlas Cloud

usr = 'christian'
pwd = 'LkipSB6LPbBV8wM'

"connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True, connect=False, maxPoolsize=1 must be add to the " \
"pymongo mongo client to get it working cause of mongo cloud db"

try:
    client = pymongo.MongoClient(
        "mongodb+srv://" + usr + ":" + pwd + "@mongodbmovie-702qa.mongodb.net/test?retryWrites=true&w=majority",
        connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True, connect=False, maxPoolsize=1)

    db = client['masterproject']
    # variable for writing poll data
    collection = db['survey']
    # variable for getting movie data
    collection_movies = db['movies']
    collection_questions = db['questions']
    print("Connected to DB succesfully!")
except:
    print(
        "Could not connect to MongoDB. Write an E-Mail to chschusc@edu.aau.at with your IP-address to get access to "
        "the database")

print("1")


@app.route('/set-/')
def set_variables(mode):
    session['mode'] = mode
    return redirect(url_for('index'))


@app.route('/get_survey')
# displays the data of the surveys collection
def get_surveys():
    documents = collection.find()
    response = []
    for document in documents:
        document['_id'] = str(document['_id'])
        response.append(document)
        response.append("<br/>")
        response.append("<br/>")
    return json.dumps(response, indent=4, sort_keys=True, default=str)


@app.route('/generate_files')
def pandas():
    try:
        client = pymongo.MongoClient(
            "mongodb+srv://" + usr + ":" + pwd + "@mongodbmovie-702qa.mongodb.net/test?retryWrites=true&w=majority")
        db = client['masterproject']
        # variable for writing poll data
        collection = db['survey']
        # variable for getting movie data
        # at the moment not used, but variable could be used for further features, like to generate lists for all movies,
        # exporting data and so on
        collection_movies = db['movies']
        collection_questions = db['questions']
        print("Connected to DB succesfully!")
    except:
        print("Could not connect to MongoDB. Write an E-Mail to chschusc@edu.aau.at with your IP-address to get "
              "access to the database")

    cursor = collection.find()
    mongo_docs = list(cursor)

    print("total docs in collection:", collection.count_documents({}))

    # create an empty DataFrame for storing documents
    docs = pd.DataFrame(columns=[])

    # iterate over the list of MongoDB dict documents
    for num, doc in enumerate(mongo_docs):
        # convert ObjectId() to str
        doc["_id"] = str(doc["_id"])

        # get document _id from dict
        doc_id = doc["_id"]

        # create a Series obj from the MongoDB dict
        series_obj = pd.Series(doc, name=doc_id)

        # append the MongoDB Series obj to the DataFrame obj
        docs = docs.append(series_obj)

        # export MongoDB documents to a CSV file
        docs.to_csv("object_rocket.csv", ",")  # CSV delimited by comma
        docs.to_excel("object_rocket.xlsx", ",")

        # export MongoDB documents to CSV
        csv_export = docs.to_csv(sep=",")  # CSV delimited by commas

        print("\nCSV data:", csv_export)

    return "MongoDB data exported successful as CSV/XLSX - File in root folder "


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
    global collection
    collection.drop()
    return "Collection survey dropped"


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


@app.route('/conditions.html')
def conditions():
    return render_template('/conditions.html', thing_to_say='Click here to start')


@app.route('/welcome.html')
def welcome():
    ##return '<a href=' + url_for("hello", name="World") + '> Lass dich grüßen</a>'
    return render_template('/welcome.html', thing_to_say='Click here to start')


@app.route('/')
def task_description():
    ##return '<a href=' + url_for("hello", name="World") + '> Lass dich grüßen</a>'
    global date_page_task_description_1

    # to clear the session
    session.clear()
    session['warning'] = 0
    # timestamp
    date_page_task_description_1 = datetime.datetime.utcnow()
    session["date_page_task_description_1"] = datetime.datetime.utcnow()
    print(session)
    session['check_shuffling'] = 0

    return render_template('/task_description.html', font_url='http://fonts.googleapis.com/css?family=PT+Sans:400,700')


@app.route('/pref_movies.html', methods=['POST', 'GET'])
def pref_movies():
    global date_page_pref_movie_2, page, allprefmovies_number, allprefmovies_number
    # for loading data into the HTML page (for example title, cover, stars ...)
    global allprefmovies
    # for getting the survey data (like/dislike/unknown)
    global preferred_movies
    # variable for generating the "you liked: " - feature
    global user_likes_movies
    # stores the likes, dislikes and neutral thumbs of the user in form of a list
    global likes_list, dislikes_list, neutral_list
    global fake, check_shuffling

    # for assignment to the right page
    session['Form_Type'] = 1

    count_page_1 = collection.count_documents({"Form_Type": 1})
    count_page_2 = collection.count_documents({"Form_Type": 2})

    print("form type 1:", count_page_1)
    print("form type 2:", count_page_2)

    if count_page_1 <= count_page_2:
        session['Form_Type'] = 1
        page = 1
        print("got selected")
    else:
        session['Form_Type'] = 2
        page = 2

    # variable for storing 2 variable
    user_preferences = []

    fake = False

    likes_list.clear()
    dislikes_list.clear()
    neutral_list.clear()

    allprefmovies.clear()
    preferred_movies.clear()

    dbmovies = db['movies']

    for movies in dbmovies.find({'type': 'pref'}, {"_id": False}):
        allprefmovies.append(movies)

    fake_movie = allprefmovies.pop()

    # cut the list from database only to 25 movies for the html page
    # allprefmovies = allprefmovies[25:]

    # for randomizing the movie list
    random.shuffle(allprefmovies)

    allprefmovies.insert(3, fake_movie)

    # variable for saving the list that the user got displayed
    if session['check_shuffling'] == 0:
        allprefmovies_number = ['']

        j = 0
        for i in allprefmovies:
            if j == 0:
                allprefmovies_number[0] = (i['number'])
            else:
                allprefmovies_number.append(i['number'])
            j += 1

    session['check_shuffling'] = 1

    print("allppref_movie after: ", str(allprefmovies_number))
    session['allprefmovies'] = allprefmovies_number

    session['date_page_pref_movie_2'] = datetime.datetime.utcnow()

    if request.method == 'POST':
        # to get the html input, passed in this list variable
        print('allpref_movies length', len(allprefmovies))
        for n in range(1, len(allprefmovies)):
            preferred_movies.append(str(request.form.get('q_pref_movies[' + str(n) + ']')))

        for n in range(1, len(allprefmovies) - 1):
            # print(str(preferred_movies[n]))
            if preferred_movies[n - 1] == 'Like':
                likes_list.append(n)
            elif preferred_movies[n - 1] == 'Dislike':
                dislikes_list.append(n)
            elif preferred_movies[n - 1] == 'Neutral':
                neutral_list.append(n)

        session['likes_list'] = list(likes_list)
        session['dislikes_list'] = list(dislikes_list)
        session['neutral_list'] = list(neutral_list)

        # variable geht die bewertete movieliste durch und speichert index/number in array.
        # this array will be used for displaying the movie in the next page

        user_likes_movies = []

    if request.method == 'POST':

        print("preferred_movies + " + str(preferred_movies))
        print("user_preferences + " + str(user_preferences))
        print("user likes movies + " + str(user_likes_movies))

        # will be exectued after form pref_movie_form is committed
        # this if checks if the popeye movie is selected and adds it to the list for the next
        if preferred_movies[0] == 'Like':
            user_preferences.append(1)

        print("preferred_movies count: ", preferred_movies.count("Like"))

        if preferred_movies.count("Like") <= 1:
            print("Yes, 'Like' NOT found in List : ", preferred_movies)
            print("Warning value before" + str(session['warning']))
            session['warning'] = 1
            print("Warning value after" + str(session['warning']))
            flash("Not enough movies have been selected: Select atleast two movies you like.")

            return redirect(url_for('pref_movies'))
        else:
            # print("Warning value before" + str(session['warning']))
            # session['warning'] = request.form['warning']
            # print("Warning value after" + str(session['warning']))
            for n in range(1, len(allprefmovies)):
                print("pref movies: " + preferred_movies[n])
                if preferred_movies[n] == 'Like':
                    # n + 1 generates the right "number" and fills user_preferences with two numbers
                    user_preferences.append(n + 1)
                    if len(user_preferences) == 2:
                        # if 2 likes found, end for loop
                        break

            try:
                for n in range(0, 2):
                    # print("user_preferences:" + str(user_preferences[n]))
                    for movies in dbmovies.find({'number': user_preferences[n], 'type': "pref"}, {"_id": False}):
                        user_likes_movies.append(movies)
            except IndexError as error:
                print(error)

            session['user_likes_movies'] = list(user_likes_movies)

            if page == 1:
                return redirect(url_for('rec_movies_1'))
            else:
                return redirect(url_for('rec_movies_2'))

    return render_template('/pref_movies.html', movie=allprefmovies)


@app.route('/rec_movies_1.html', methods=['POST', 'GET'])
def rec_movies_1():
    # list with 10 objects
    global page, allsuggmovies
    global user_likes_movies, user_likes_movies, user_preferences
    dbmovies = db['movies']

    allsuggmovies.clear()

    # querying all titles
    # for x in range(0, sugg_numMovies):
    for movies in dbmovies.find({'type': 'rec'}, {"_id": False}):
        allsuggmovies.append(movies)

    # for randomizing the movie list
    random.shuffle(allsuggmovies)

    session['date_page_rec_movie_3'] = datetime.datetime.utcnow()

    if request.method == 'POST':
        session['watchlist'] = request.form.getlist('q_Watchlist')
        session['favourite'] = str(request.form.get('q23_bestRecommended'))

    if request.method == 'POST':
        return redirect(url_for('questionnaire'))

    return render_template('/rec_movies_1.html', movie=allsuggmovies, user_pref=session['user_likes_movies'])


@app.route('/rec_movies_2.html', methods=['POST', 'GET'])
def rec_movies_2():
    # list with 10 objects
    global page, allsuggmovies
    global user_likes_movies, user_likes_movies, user_preferences
    dbmovies = db['movies']

    allsuggmovies.clear()

    # querying all titles
    # for x in range(0, sugg_numMovies):
    for movies in dbmovies.find({'type': 'rec'}, {"_id": False}):
        allsuggmovies.append(movies)

    # for randomizing the movie list
    random.shuffle(allsuggmovies)
    session['date_page_rec_movie_3'] = datetime.datetime.utcnow()

    if request.method == 'POST':
        session['watchlist'] = request.form.getlist('q_Watchlist')
        session['favourite'] = str(request.form.get('q23_bestRecommended'))

    if request.method == 'POST':
        return redirect(url_for('questionnaire'))

    return render_template('/rec_movies_2.html', movie=allsuggmovies, user_pref=session['user_likes_movies'])


@app.route('/questionnaire.html', methods=['POST', 'GET'])
def questionnaire():
    global date_page_questionnaire_4
    global questionnaire_answer_from_survey, questionnaire_answer_from_survey_pers, questions_rec
    global questions_pers

    dbquestions = db['questions']

    questions_rec = []
    questions_pers = []
    # print("questions_rec: " + str(questions_rec))
    # print("questions_pers: " + str(questions_pers))
    # dbquestions = db['questions']

    allquestions_from_db_rec.clear()
    allquestions_from_db_pers.clear()

    # to get the questions about the recommended systems
    for questions_rec in dbquestions.find({'type': "rating_rec"}):
        allquestions_from_db_rec.append(questions_rec)

    # last question in mongodb is the fake question
    fake_question = allquestions_from_db_rec.pop()

    allquestions_from_db_rec.insert(5, fake_question)

    # to get the questions about the personality
    for questions_pers in dbquestions.find({'type': "rating_pers"}):
        allquestions_from_db_pers.append(questions_pers)

    # to get the questions about the personality
    session['date_page_questionnaire_4'] = datetime.datetime.utcnow()

    # random.shuffle(allquestions_from_db_rec)

    # print('len(allquestions_from_db_rec)', len(allquestions_from_db_rec))
    questionnaire_answer_from_survey.clear()
    questionnaire_answer_from_survey_pers.clear()
    # print("preferred_movies Ergebnis" + str(questionnaire_answer_from_survey))

    if request.method == 'POST':
        # to get the answered survey data about the recommended system
        for n in range(1, len(allquestions_from_db_rec) + 1):
            questionnaire_answer_from_survey.append(str(request.form.get('q_survey_rec_[' + str(n) + ']')))
            print("questions rec " + str(n) + " " + str(questionnaire_answer_from_survey))

        for n in range(1, len(allquestions_from_db_pers) + 1):
            questionnaire_answer_from_survey_pers.append(str(request.form.get('q_survey_pers_[' + str(n) + ']')))
            print("questions pers " + str(n) + " " + str(questionnaire_answer_from_survey_pers))

        session['questionnaire_answer_from_survey'] = list(questionnaire_answer_from_survey)
        session['questionnaire_answer_from_survey_pers'] = list(questionnaire_answer_from_survey_pers)

        print("questions rec: " + str(session['questionnaire_answer_from_survey_pers']))
        print("questions pers" + str(session['questionnaire_answer_from_survey_pers']))

        session['feedbacktext'] = str(request.form.get('feedbacktext'))
        session['age'] = str(request.form.get('age'))
        session['gender'] = str(request.form.get('gender'))
        return redirect(url_for('end'))

    return render_template('/questionnaire.html', questions=allquestions_from_db_rec,
                           questions_pers=allquestions_from_db_pers)


@app.route('/end.html', methods=['POST', 'GET'])
def end():
    ## Assignment of the resulted input of the html variables
    ## contains all data of the survey

    global page, preferred_movies
    global questionnaire_answer_from_survey, questionnaire_answer_from_survey_pers
    global likes_list, dislikes_list, neutral_list, fake
    global date_page_task_description_1, date_page_pref_movie_2, date_page_rec_movie_3, date_page_questionnaire_4
    global watchlist, questions_rec, questions_pers, gender, age, feedbacktext

    # these two loops are for checking the likes and dislike list if the user picked the fake movie popeye
    # in mongodb popeye has the number 1
    session['retention_check_1_passed'] = True

    for n in range(0, len(session['likes_list']) - 1):
        if session['likes_list'][n] == 1:
            session['retention_check_1_passed'] = False

    for n in range(0, len(session['dislikes_list']) - 1):
        if session['likes_list'][n] == 1:
            session['retention_check_1_passed'] = False

    # this for loop is for checking the questionnaire list if the user picked the fake question "This question should
    # be rated as 2" if he picks not 2, it is marked as fake in mongodb
    session['retention_check_2_passed'] = False

    for n in range(1, len(questionnaire_answer_from_survey)):
        #    print('questionnaire_answer_from_survey[' + str(n) + '] ' + str(questionnaire_answer_from_survey[n]))
        # if questionnaire_answer_from_survey[19] != "2":
        #     fake = True
        if session['questionnaire_answer_from_survey'][19] == "2":
            fake = True
            session['retention_check_2_passed'] = True

    session['date_page_submit_5'] = datetime.datetime.utcnow()

    ## fuction for saving all data in mongo database
    message = save()

    # for the next user, so user 1 gets List 1, User 2 gets List 2, and so on
    if page == 1:
        page = 2
    else:
        page = 1

    return message


def save():
    """
    Saving in Cloud Atlas MongoDB
    """

    # variable n shows which page is used, if n is == 2 then user got list 2, is n == 1 then user got List 1
    # idea is to merge to two lists to get one dictionary for inserting survey data in db
    # this list variable is for the left part of the dictionary (for example "pre_movie_0")
    questions_rec_attributename = []
    questions_pers_attributename = []

    questions_pers_attributename.clear()

    # to create attributes name for mongo db
    for x in range(1, len(session['questionnaire_answer_from_survey']) + 1):
        if x < 10:
            questions_rec_attributename.append('Question_Rec_0' + str(x))
        else:
            questions_rec_attributename.append('Question_Rec_' + str(x))

    for x in range(1, len(session['questionnaire_answer_from_survey_pers']) + 1):
        if x < 10:
            questions_pers_attributename.append('Question_Pers_0' + str(x))
        else:
            questions_pers_attributename.append('Question_Pers_' + str(x))

    # https://docs.python.org/2/tutorial/datastructures.html#list-comprehensions
    print("questions_pers_attributename ", str(questions_pers_attributename))

    # using the dictionary form to input data in mongodb

    if session['warning'] == 0:
        warning = False
    else:
        warning = True

    new = {
        "Form_Type": session['Form_Type'],
        "Gender": session['gender'],
        "Age": session['age'],
        "Timestamp_start_session": session['date_page_task_description_1'],
        "Timestamp_page_2": session['date_page_pref_movie_2'],
        "Timestamp_page_3": session['date_page_rec_movie_3'],
        "Timestamp_page_4": session['date_page_questionnaire_4'],
        "Timestamp_page_submit": session['date_page_submit_5'],
        "Next_Movie_To_Watch": session['favourite'],
        "Watchlist": session['watchlist'],
        'Like': session['likes_list'],
        'Dislike': session['dislikes_list'],
        'Neutral': session['neutral_list'],
        "Feedback_Text": session['feedbacktext'],
        "retention_check_1_passed": session['retention_check_1_passed'],
        "retention_check_2_passed": session['retention_check_2_passed'],
        "warning_occured": session['warning'],
        "displayed_list_pref_movies": session['allprefmovies']
    }
    # list comprehension to write
    new.update(dict(zip(questions_rec_attributename, session['questionnaire_answer_from_survey'])))
    new.update(dict(zip(questions_pers_attributename, session['questionnaire_answer_from_survey_pers'])))

    try:
        ## Creates a new document in DB
        # creates a new ID for json-file in mongodb
        session_id = collection.insert_one(new)
        print("database entry successfully")
    except:
        print("database entry not successfully!")
    # returns a successful message if successful
    print("db entry " + str(new) + " was successfully inserted in database")
    print("to see output --> http://127.0.0.1:5000/get_survey")
    print("to generate csv/xlsx data --> http://127.0.0.1:5000/generate_files - Files be located in root folder of"
          " the project")

    entry = "db entry was successfully inserted in database!"
    entry += '\n' + " "
    message = "to see output: "
    links = "to generate csv/xlsx data: "
    output = entry + '\n' + message
    return render_template('/end.html', message=output, links=links)


if __name__ == '__main__':
    app.run(debug=True)
