# Poll App

CHANGES 26.03.2020:
     
     changed checkbox/radiobuttons
     position of retentionchecks
    
NEXT CHANGES SOON:

    clean up the code
 

The idea behind this project is to make first experiences with **Mongodb, pymongo, virtuelenv** and **flask**.
It contains a study which results will be inserted into the database.
 

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
###### deploying flask server on ubuntu

##### Step One— Install and Enable mod_wsgi

Open terminal and type the following command to install mod_wsgi:
```
$ sudo apt-get install libapache2-mod-wsgi python-dev
```

To enable mod_wsgi, run the following command:
```
$ sudo a2enmod wsgi 
```
##### Step Two – Creating a Flask App

[FQDN] = Full qualified domain name, name of the server

```
cd /var/[FQDN]/www
sudo mkdir FlaskApp
cd FlaskApp
sudo mkdir FlaskApp

```
Your directory structure should now look like this:

|----FlaskApp  
|---------FlaskApp  
|--------------static  
|--------------templates  

download repository via git:

```
git clone https://github.com/chrisschu/Poll_App.git
```
#### Step Three – Install Flask

sudo apt-get install python-pip 
sudo pip install virtualenv 
sudo virtualenv venv

source venv/bin/activate

pip install -r requirements.txt
sudo pip install Flask 

Next, run the following command to test if the installation is successful and the app is running:

sudo python app.py

It should display “Running on http://localhost:5000/” or "Running on http://127.0.0.1:5000/". 
If you see this message, you have successfully configured the app.

To deactivate the environment, give the following command:
````
deactivate
````



#### Step Four – Configure and Enable a New Virtual Host

sudo vim /etc/apache2/sites-available/Poll_App.conf

    <VirtualHost *:80>
		ServerName mywebsite.com
		ServerAdmin admin@mywebsite.com
		WSGIScriptAlias / /var/[FQDN]/www/FlaskApp/flaskapp.wsgi
		<Directory /var/[FQDN]/www/FlaskApp/Poll_App/>
			Order allow,deny
			Allow from all
		</Directory>
		Alias /static /var/[FQDN]/FlaskApp/Poll_App/static
		<Directory /var/[FQDN]/FlaskApp/Poll_App/static/>
			Order allow,deny
			Allow from all
		</Directory>
		ErrorLog ${APACHE_LOG_DIR}/error.log
		LogLevel warn
		CustomLog ${APACHE_LOG_DIR}/access.log combined
    </VirtualHost>

save and close

#### Step Four – Configure and Enable a New Virtual Host

Enable the virtual host with the following command:
````
sudo a2ensite FlaskApp
````

##### Step Five – Create the .wsgi File

Apache uses the .wsgi file to serve the Flask app. Move to the /var/www/FlaskApp directory and create a file named flaskapp.wsgi with following commands:
````
cd /var/[FQDN]/www/FlaskApp
sudo vim flaskapp.wsgi 
````
Add the following lines of code to the flaskapp.wsgi file:
````
#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/FlaskApp/")

from FlaskApp import app as application
application.secret_key = 'Add your secret key'
````
Now your directory structure should look like this:
--------------
|--------FlaskApp  
|----------------Poll_app  
|-----------------------static  
|-----------------------templates  
|-----------------------venv  
|-----------------------app.py  
|----------------flaskapp.wsgi  

##### Step Six – Restart Apache

Restart Apache with the following command to apply the changes:
````
sudo service apache2 restart 
````
You may see a message similar to the following:

Could not reliably determine the VPS's fully qualified domain name, using 127.0.0.1 for ServerName 
This message is just a warning, and you will be able to access your virtual host without any further issues. To view your application, open your browser and navigate to the domain name or IP address that you entered in your virtual host configuration.

You have successfully deployed a flask application.

**Source:**

https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps