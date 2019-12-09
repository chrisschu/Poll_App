from flask import Flask, render_template, request
from flask_mongoengine import MongoEngine

## Author Christian Schuschnig

app = Flask(__name__)
##app.config["MONGO_URI"] = "mongodb+srv://christian:LkipSB6LPbBV8wM@mongodbmovie-702qa.mongodb.net/test?retryWrites" \
##                          "=true&w=majority "
##mongo = PyMongo(app)

@app.route('/')
def index():
    ##return '<a href=' + url_for("hello", name="World") + '> Lass dich grüßen</a>'
    return render_template('poll.html',thing_to_say='Click here to start')

@app.route('/hello/<path:name>')
def hello(name):
    return 'Hello ' + name + ' ! '


##@app.route("/db")
## def home_page():
##    online_users = mongo.db.users.find({"online": True})
##    return render_template("index.html",
##        online_users=online_users)


@app.route('/my_form', methods=['POST'])
def my_form():
    question1 = request.form['question1']
    question2 = request.form['question2']
    dropdown1 = request.form['dropdown1']
    dropdown2 = request.form['dropdown2']
    textbox = request.form['textbox']

    dictionary = {"question1":question1, "question2" : question2, "dropdown1": dropdown1, "dropdown2": dropdown2, "textbox": textbox}

    # Now that get value back to server can send it to a DB(use Flask-SQLAlchemy)
    return dictionary


if __name__ == '__main__':
    app.run(debug=True)
