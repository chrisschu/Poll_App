# Poll App

This is a simple polling app. 

The idea behind this project is to make first experiences with **Mongodb, pymongo, virtuelenv** and **flask**.
It contains a simple questionnaire which results will be inserted into the database.
 
At the moment this app offers only insertion, not viewing the database. 

As database the cloud solution **MongoDB Atlas** will be used.

## Steps for deployment

I used PyCharm.
Tutorial is written for Windows/Linux.

### Python
**Python 3** is required.

```bash
# make sure you have Python 3
python --version
```
### PIP

```bash
# make sure pip is installed
pip --version

# install pip3 otherwise
python -m pip --version
```
if pip is not installed: 
```bash

To install pip, securely download get-pip.py. 1:

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
Then run the following:
python get-pip.py
```bash
```
### Create a Virtual Python Environment
cd to your project directory and run virtualenv to create the new virtual environment.

The following commands will create a new virtual environment under Poll_App/my-venv.

```bash
cd Poll_App
virtualenv --python C:\Path\To\Python\python.exe venv
```

### Activate virtual environment

Linux:
```bash
source env/bin/activate
```
Windows:
```bash
source .\venv\Scripts\activate
```
### Install dependencies

```bash
(venv) pip install -r requirements.txt
```

### Start the app
for Linux based OS:

```bash
$ export FLASK_APP=app.py
```

for Windows (cmd):
```bash
$ set FLASK_APP=app.py
```
```bash
$ python -m flask run
 * Running on http://127.0.0.1:5000/
```

App is now accessible via http://127.0.0.1:5000/