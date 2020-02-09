import datetime

import pymongo
from flask import Flask, render_template, request, url_for, redirect
from pymongo import *

## Author Christian Schuschnig

# Application contains global variables cause the split of the html files

## first decleration of global variables


# variable for timestamps
date_page_task_description_1 = ''
date_page_pref_movie_2 = ''
date_page_rec_movie_3 = ''
date_page_questionnaire_4 = ''
date_page_submit_5 = ''

pre_movie_0 = "X"
pre_movie_1 = 'X'
pre_movie_2 = 'X'
pre_movie_3 = 'X'
pre_movie_4 = 'X'

suggested_movie_1 = 'X'
suggested_movie_2 = 'X'
suggested_movie_3 = 'X'
suggested_movie_4 = 'X'
suggested_movie_5 = 'X'
suggested_movie_6 = 'X'

favourite = 'X'
poll_q1 = 'X'
poll_q2 = 'X'
poll_q3 = 'X'

#this variable is roundrobin princible, first user gets page 1, second user gets page 2, and so on
page = 1

app = Flask(__name__)

## Connection to the MongoDB Atlas Cloud
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
##Routing to old poll, just for testing
def poll():
    ##return '<a href=' + url_for("hello", name="World") + '> Lass dich grüßen</a>'
    return render_template('poll.html', thing_to_say='Click here to start')


@app.route('/welcome.html')
def Movie_poll():
    ##return '<a href=' + url_for("hello", name="World") + '> Lass dich grüßen</a>'
    return render_template('/Movie-Poll.html', thing_to_say='Click here to start')


@app.route('/my_form', methods=['POST'])
##old poll app, just for testing
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
    date_page_task_description_1 = datetime.datetime.utcnow()

    return render_template('/task_description.html', thing_to_say='Click here to start')


@app.route('/pref_movies.html', methods=['POST', 'GET'])
def pref_movies():
    global pre_movie_0, pre_movie_1, pre_movie_2, pre_movie_3, pre_movie_4, date_page_pref_movie_2, page

    date_page_pref_movie_2 = datetime.datetime.utcnow()

    pre_movie_0 = str(request.form.get('q4_overallSatisfaction[0]'))
    pre_movie_1 = str(request.form.get('q4_overallSatisfaction[1]'))
    pre_movie_2 = str(request.form.get('q4_overallSatisfaction[2]'))
    pre_movie_3 = str(request.form.get('q4_overallSatisfaction[3]'))
    pre_movie_4 = str(request.form.get('q4_overallSatisfaction[4]'))

    if request.method == 'POST':
        # will be exectued after form pref_movie_form is commited
        if page == 1:
            # 50 per cent chance to have the first list with 10 objects
            return redirect(url_for('rec_movies_1'))
        else:
            # 50 per cent chance to have the first list with 12 objects
            return redirect(url_for('rec_movies_2'))

    return render_template('/pref_movies.html', thing_to_say='Click here to start')


@app.route('/rec_movies_1.html', methods=['POST', 'GET'])
def rec_movies_1():
    # list with 10 objects
    global suggested_movie_1, suggested_movie_2, suggested_movie_3, suggested_movie_4, suggested_movie_5, \
        suggested_movie_6, favourite, date_page_rec_movie_3, page

    date_page_rec_movie_3 = datetime.datetime.utcnow()

    suggested_movie_1 = str(request.form.get('q20_movies20[0]'))
    suggested_movie_2 = str(request.form.get('q20_movies20[1]'))
    suggested_movie_3 = str(request.form.get('q20_movies20[2]'))
    suggested_movie_4 = str(request.form.get('q20_movies20[3]'))
    suggested_movie_5 = str(request.form.get('q20_movies20[4]'))
    suggested_movie_6 = str(request.form.get('q20_movies20[5]'))

    favourite = str(request.form.get('q23_bestRecommended'))

    if request.method == 'POST':
        #next user gets page rec_movies_2.html
        page = 2
        return redirect(url_for('questionnaire'))

    return render_template('/rec_movies_1.html', thing_to_say='Click here to start')


@app.route('/rec_movies_2.html', methods=['POST', 'GET'])
def rec_movies_2():
    # list with 10 objects + 2 additional objects
    global suggested_movie_1, suggested_movie_2, suggested_movie_3, suggested_movie_4, suggested_movie_5, \
        suggested_movie_6, favourite, date_page_rec_movie_3, page

    date_page_rec_movie_3 = datetime.datetime.utcnow()

    suggested_movie_1 = str(request.form.get('q20_movies20[0]'))
    suggested_movie_2 = str(request.form.get('q20_movies20[1]'))
    suggested_movie_3 = str(request.form.get('q20_movies20[2]'))
    suggested_movie_4 = str(request.form.get('q20_movies20[3]'))
    suggested_movie_5 = str(request.form.get('q20_movies20[4]'))
    suggested_movie_6 = str(request.form.get('q20_movies20[5]'))

    favourite = str(request.form.get('q23_bestRecommended'))

    if request.method == 'POST':
        # next user gets page rec_movies_1.html
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
        suggested_movie_3, suggested_movie_4, suggested_movie_5, suggested_movie_6, favourite, poll_q1, poll_q2, \
        poll_q3

    global date_page_task_description_1, date_page_pref_movie_2, date_page_rec_movie_3, date_page_questionnaire_4
    global date_page_submit_5

    date_page_submit_5 = datetime.datetime.utcnow()

    ## saving in mongodb
    save(page, pre_movie_0, pre_movie_1, pre_movie_2, pre_movie_3, pre_movie_4, suggested_movie_1, suggested_movie_2,
         suggested_movie_3, suggested_movie_4, suggested_movie_5, suggested_movie_6, favourite, poll_q1, poll_q2,
         poll_q3,
         date_page_task_description_1, date_page_pref_movie_2, date_page_rec_movie_3,
         date_page_questionnaire_4, date_page_submit_5)

    return "Db entry successful"


def save(pre_movie_0_x, pre_movie_1_x, pre_movie_2_x, pre_movie_3_x, pre_movie_4_x, suggested_movie_1_x,
         suggested_movie_2_x, suggested_movie_3_x, suggested_movie_4_x, suggested_movie_5_x, suggested_movie_6_x,
         favourite_x, poll_q1_x,
         poll_q2_x, poll_q3_x, date_page_task_description_1_x, date_page_pref_movie_2_x, date_page_rec_movie_3_x,
         date_page_questionnaire_4_x, date_page_submit_5_x):
    """
    Saving in Cloud Atlas MongoDB
    """

    new = {
        "Form": page,
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


def roundrobin_page():
    #
    pass


if __name__ == '__main__':
    app.run(debug=True)
