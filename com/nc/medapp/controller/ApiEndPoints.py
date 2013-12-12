'''
Created on 01-Dec-2013

@author: blackpearl
'''

from flask import Flask
from flask import request,abort,render_template,Response
from flask.ext.mail import Mail
from flask.ext.mail import Message
from com.nc.medapp.util.Mailer import Mailer
from com.nc.medapp.api.LoginResource import LoginResource
from com.nc.medapp.config import *
from com.nc.medapp.model.DBMapper import User,Speciality,Session
import json
from mongoengine import *
import string
import random


app = Flask("MedApp")
connect('test')
app.config.update(dict(
     DEBUG = True,
     MAIL_SERVER = 'smtp.gmail.com',
     MAIL_PORT = 587,
     MAIL_USE_TLS = True,
     MAIL_USE_SSL = False,
     MAIL_USERNAME = 'simplychampak@gmail.com',
     MAIL_PASSWORD = 'CounterStrike@123',
 ))
mail = Mail(app)


############### ACCOUNT API'S ############### 
@app.route('/account/login',methods=['POST'])
def login():
    validateJSON(request.json)
    email = request.json['email']
    password = request.json['password']
    user = User.objects(email=email).first()
    if user:
        if user.password == password :
            if user.enabled == False:
                ret = '{"status":"FAILED","message":"ACCOUNT NOT ACTIVATED, PLEASE ACTIVATE FROM EMAIL"}'
                resp = Response(response=ret,status=200,mimetype="application/json")
                return resp
            token = generateToken()
            headers = {}
            headers['appToken']=token
            ret = '{"status":"SUCCESS"}'
            resp = Response(response=ret,status=200,mimetype="application/json",headers=headers)            
            return resp
        else :
            ret = '{"status":"FAILED","message":"INVALID PASSWORD / USER"}'
            resp = Response(response=ret,status=200,mimetype="application/json")
            return resp
    else:
        ret = '{"status":"FAILED","message":"INVALID PASSWORD / USER"}'
        resp = Response(response=ret,status=200,mimetype="application/json")
        return resp

@app.route('/account/register',methods=['POST'])
def register():
    validateJSON(request.json)
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')
    speciality = request.json.get('speciality')
    # Fetch speciality object reference
    spec = Speciality.objects(fieldname=speciality).first()
    # Create a user object and save to DB
    user = User(name=name,email=email,password=password,speciality=spec.id)
    try:
        user.save()
    except NotUniqueError as e:
        ret = '{"status":"FAILED","message":"USER ALREADY REGISTERED"}'
        return Response(response=ret,status=200,mimetype="application/json")
    except ValidationError as email:
        ret = '{"status":"FAILED","message":"EMAIL VALIDATION ERROR"}'
        return Response(response=ret,status=200,mimetype="application/json")
    # Create and save a temp token
    session = Session(user.id)
    session.save()
    token = str(session.id)
    # Shoot a registration email
    sendRegistraionEmail(user,token)
    # Return a response
    ret = '{"status":"SUCCESS","message":"User Registered Successfully"}'
    return Response(response=ret,status=200,mimetype="application/json")


@app.route('/account/specialities')
def getSpecialities():
    specialities = Speciality.objects
    temp_list=[]
    for speciality in specialities:
        temp_list.append(speciality.fieldname)
    
    return json.dumps(temp_list) 

@app.route('/account/forgotPassword',methods=['POST'])
def forgotPassword():
    return "Forgot Password"

    
@app.route('/account/activate/<token>')
def activate(token):
    tok = Session.objects(id=token).first()
    if not tok:
        return json.dumps([{"status":"Token invalid or account is already activated"}])
    else:
        if token == str(tok.id):
            user = User.objects(id=str(tok.user.id)).first()
            user.enabled=True
            user.save()
            tok.delete()
        else :
            return json.dumps([{"status":"Token invalid or account is already activated"}])
        
    return json.dumps([{"status":"Account activated successfully"}])

# Helper methods
def validateJSON(json):
    if not json:
        abort(401)


def sendRegistraionEmail(user,token):
    mailer = Mailer(mail)
    mailUser = {}
    mailUser['name'] = user.name
    mailUser['token'] = token
    mailer.send_email("Welcome to MED APP application", [user.email], render_template("register.tmpl",user=mailUser), render_template("register.tmpl",user=mailUser))


def generateToken():
    return ''.join(random.choice(string.ascii_uppercase) for i in range(12))
 
if __name__ == '__main__':
    app.run()
    