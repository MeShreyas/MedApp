'''
Created on 01-Dec-2013

@author: blackpearl
'''

from flask import Flask
from flask import request,abort,render_template,Response
from com.nc.medapp.model.DBMapper import User, Speciality, Session, Token
from com.nc.medapp.exception.ValueError import MedAppValueError
from mongoengine import *
from com.nc.medapp.util.Helper import validateJSON, generateToken
import json

def login():
    validateJSON(request.json)
    email = request.json['email']
    password = request.json['password']
    user = User.objects(email=email).first()
    if user:
        if user.password == password :
            if user.enabled == False:
                ret = '{"status":"Fail","message":"User not activated or not registered"}'
                resp = Response(response=ret,status=401,mimetype="application/json")
                return resp
            token = generateToken()
            headers = {}
            headers['appToken']=token
            token = Token(user = user,token=token)
            try:
                token.save()
            except Exception, e:
                ret = '{"status":"Fail","message":"Failed to save user token"}'
                resp = Response(response=ret,status=500,mimetype="application/json",headers=headers)
                return resp
            ret = '{"status":"Success","message":"User Successfully LogIn"}'
            resp = Response(response=ret,status=200,mimetype="application/json",headers=headers)            
            return resp
        else :
            ret = '{"status":"Fail","message":"Invalid user / password"}'
            headers={}
            headers['WWW-Authenticate'] ='OAuth realm="NirmanCraft"'
            resp = Response(response=ret,status=401,mimetype="application/json",headers=headers)
            return resp
    else:
        ret = '{"status":"Fail","message":"User not activated or not registered"}'
        resp = Response(response=ret,status=401,mimetype="application/json")
        return resp

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
