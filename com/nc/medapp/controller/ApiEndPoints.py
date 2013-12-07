'''
Created on 01-Dec-2013

@author: blackpearl
'''

from flask import Flask
from flask import requests
from flask.ext.mail import Mail
from flask.ext.mail import Message
from com.nc.medapp.util import Mailer
from com.nc.medapp.api.LoginResource import LoginResource
from com.nc.medapp.config import *


app = Flask("MedApp")
# app.config.update(dict(
#     DEBUG = True,
#     MAIL_SERVER = 'smtp.gmail.com',
#     MAIL_PORT = 587,
#     MAIL_USE_TLS = True,
#     MAIL_USE_SSL = False,
#     MAIL_USERNAME = 'simplychampak@gmail.com',
#     MAIL_PASSWORD = 'CounterStrike@123',
# ))
# mail = Mail(app)


############### ACCOUNT API'S ############### 
@app.route('/account/login',methods=['POST'])
def login():
    # Get the request here. As they are post parameters fetching from request
    if requests.json[USERNAME] is not None:
        user = User()
    return "Hello World"

@app.route('/account/register',methods=['POST'])
def register():
    return "Register User"

@app.route('/account/forgotPassword',methods=['POST'])
def forgotPassword():
    return "Forgot Password"

@app.route('/account/changePassword',methods=['POST'])
def changePassword():
    return "Change Password"
    

    
# @app.route('/')
# def helloWorld():
#     
#     Mailer.send_email("Hello Workd", "patilshreyas27@gmail.com", "simplychampak@gmail.com", "You Rock", "You Rock")
#     return "Hello MedApp"


if __name__ == '__main__':
    app.run()
    