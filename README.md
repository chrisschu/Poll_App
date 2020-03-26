# Poll App

LAST CHANGE: 01.03.2020

    little design changes
    "You liked" - Feature working
    beginning of new questionnaire

NEXT CHANGES SOON:

    further work in questionnaire needed
    watchlist will be written in mongodb
    variable names will be clearer
 

The idea behind this project is to make first experiences with **Mongodb, pymongo, virtuelenv** and **flask**.
It contains a questionnaire which results will be inserted into the database.
 

As database the cloud solution **MongoDB Atlas** will be used.

## Steps for deployment

I used PyCharm.
Tutorial is written for Windows/Linux.

## PyCharm Settings

![PyCharm-Configuration](https://raw.githubusercontent.com/chrisschu/Poll_App/master/static/PyCharm_Settings.PNG)


### Python
**Python 3** is required.

```bash
# make sure you have Python 3
python --version
```
If not install it and set up the environment variable:

    How to set up environment variable for python:
    https://datatofish.com/add-python-to-windows-path/


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
```
Windows\Powershell
```
python get-pip.py.
```
### Create a Virtual Python Environment
cd to your project directory and run virtualenv to create the new virtual environment.

The following commands will create a new virtual environment under Poll_App/my-venv.
Linux/Bash:
```bash
change to Poll_App - Directory
cd Poll_App
```

Win10/Powershell
```
cd Poll_App 
pip install virtualenv
virtualenv venv
```

### Activate virtual environment

Linux/Bash:
```bash
source env/bin/activate
```
Win10/Powershell

```powershell

Set-ExecutionPolicy RemoteSigned
change to yes

cd Poll_App
.\venv\Scripts/activate
```
Now (venv) should be activated
### Install dependencies

```bash
(venv) pip install -r requirements.txt
```

### Install Visual C++ Tools for PANDAS 

for Windows (powershell):

(venv) must be activated
```
execute the visualcpppbuildtools_full.exe to install the c++ tools
.\visualcppbuildtools_full.exe
```

### Start the app
for Linux based OS:

```bash
$ export FLASK_APP=app.py
```

for Windows (cmd):
```cmd
$ set FLASK_APP=app.py
```
```cmd
$ python -m flask run
 * Running on http://127.0.0.1:5000/
```

App is now accessible via http://127.0.0.1:5000/