'''
Created on 01-Dec-2013

@author: blackpearl
'''

from flask import Flask
from flask import request,abort,render_template,Response
from flask.ext.mail import Mail
from flask.ext.mail import Message
from com.nc.medapp.util.Mailer import Mailer
import dateutil.parser
from com.nc.medapp.model.DBMapper import User,Speciality,Session, Target, Token,\
    Goal,Eventtype, Event
import json
from mongoengine import *
from com.nc.medapp.exception.ValueError import MedAppValueError
import os
from com.nc.medapp.util.Helper import *
from com.nc.medapp.api import LoginResource, PhotoResource, EventResource,\
    TargetResource, UserResource


UPLOADS_FOLDER='/MedApp/images'
ALLOWED_EXTENSIONS = set(['jpg','jpeg','png','gif'])

app = Flask("MedApp")
connect('test',tz_aware = True)
app.config.update(dict(
     #MAIL_SERVER = 'smtp.gmail.com',
     MAIL_SERVER = 'smtpout.secureserver.net',
     #MAIL_PORT = 587,
     MAIL_PORT = 465,
     #EMAIL_USE_TLS = False,
     MAIL_USE_SSL = True,
     MAIL_USERNAME = 'support@shared-health.co.uk',
     #MAIL_USERNAME = 'simplychampak@gmail.com',
     #MAIL_PASSWORD = 'CounterStrike@123',
     MAIL_PASSWORD = 'Mysore1234',
 ))
#app.config['UPLOADS_DEFAULT_DEST']=UPLOADS_FOLDER
mail = Mail(app)


############### PHOTO API'S ###############
@app.route('/uploadPhoto/<eventId>',methods=['POST'])
def uploadPhoto(eventId):
    return PhotoResource.uploadPhoto(eventId);



############### EVENT API'S ###############
@app.route('/events',methods=['POST'])
def createEvent():
    return EventResource.createEvent()
    
@app.route('/events/<eventId>',methods=['PUT'])
def updateEvent(eventId):
    return EventResource.updateEvent(eventId)
    
@app.route('/events/<eventId>',methods=['GET'])
def getEvent(eventId):
    return EventResource.getEvent(eventId)

@app.route('/events',methods=['GET'])
def getEvents():
    return EventResource.getEvents()

@app.route('/events/copy/<eventId>',methods=['POST'])
def copyEvent(eventId):
    pass

@app.route('/events/invite/<eventId>/<userId>',methods=['POST'])
def sendInviteForEvent(eventId,userId):
    pass

@app.route('/eventTypes',methods=['GET'])
def getEventTypes():
    eventTypes = Eventtype.objects
    temp_list=[]
    for eventType in eventTypes:
        temp_list.append(eventType.eventType)    
    return json.dumps(temp_list) 




############### ACCOUNT API'S ############### 
@app.route('/account/login',methods=['POST'])
def login():
    return LoginResource.login()

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
        ret = '{"status":"Fail","message":"User Already Registered"}'
        return Response(response=ret,status=401,mimetype="application/json")
    except ValidationError as email:
        ret = '{"status":"Fail","message":"Standard server errors : Invalid Email"}'
        return Response(response=ret,status=401,mimetype="application/json")
    # Create and save a temp token
    session = Session(user.id)
    session.save()
    token = str(session.id)
    # Shoot a registration email
    sendRegistraionEmail(user,token)
    # Return a response
    ret = '{"status":"Success","message":"User Successfully Registered"}'
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
    ret = '{"status":"Success","message":"Password has been sent to your mailbox"}'
    return Response(response=ret,status=200,mimetype="application/json")
    
@app.route('/account/activate/<token>')
def activate(token):
    return LoginResource.activate(token)



############### TARGET API'S ############### 
@app.route('/user/targets',methods=['POST'])
def setTargets():
    return TargetResource.setTargets()

@app.route('/user/targets',methods=['GET'])
def getTargets():
    return TargetResource.getTargets()

@app.route('/user/targets/<target>',methods=['GET'])
def getTarget(target):
    return TargetResource.getTarget(target)

@app.route('/user/goals/<target>',methods=['POST'])
def setGoals(target):
    return TargetResource.setGoals(target)


############### SOCIAL API'S ###############
@app.route('/friends/search',methods=['GET'])
def searchUser():
    return UserResource.searchUser()

@app.route('/friends/<user>',methods=['POST'])
def addFriend(user):
    return UserResource.addFriend(user)

@app.route('/friends',methods=['GET'])
def getFriendList():
    return UserResource.getFriendList()

@app.route('/friends/invite/<email>',methods=['GET'])
def inviteUser(email):
    pass


def sendRegistraionEmail(user,token):
    mailer = Mailer(mail)
    mailUser = {}
    mailUser['name'] = user.name
    mailUser['token'] = token
    mailer.send_email("Welcome to MED APP application", [user.email], render_template("register.tmpl",user=mailUser), render_template("register.tmpl",user=mailUser))
 
 
 
if __name__ == '__main__':
    app.run(debug=False)
    