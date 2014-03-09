'''
Created on 01-Dec-2013

@author: blackpearl
'''
import json
from flask import Flask
from flask import request,abort,render_template,Response
from com.nc.medapp.model.DBMapper import User, Speciality, Session, Token
from com.nc.medapp.exception.ValueError import MedAppValueError
from mongoengine import *
from com.nc.medapp.util.Helper import validateJSON, generateToken,\
    validateSession


def searchUser():
    user = validateSession(request)
    if not user:
        ret = '{"status":"Fail","message":"Please login"}'
        return Response(response=ret,status=401,mimetype="application/json")
    
    name = request.args.get('name')
    email = request.args.get('email')
    speciality = request.args.get('speciality')
    
    try :
        if name:
            users = User.objects(name__contains=name)
        elif email:
            users = User.objects(email=email)
        elif speciality:
            spec = Speciality.objects(fieldname=speciality).first()
            if not spec:
                users=None
            else :
                users = User.objects(speciality=spec.id)
        else:
            users = None
    except ValidationError as e:
        users = None
        
    if users:
        userList = []
        for user in users:
            response = {}
            response['id']=str(user.id)
            response['name']=user.name
            response['email']=user.email
            response['speciality']=user.speciality.fieldname
            userList.append(response)
        ret = json.dumps(userList);
    else:
        ret = '{"status":"Error","message":"No Users Found"}'
    return Response(response=ret,status=200,mimetype="application/json")   

     
def addFriend(friend):
    user = validateSession(request)
    if not user:
        ret = '{"status":"Fail","message":"Please login"}'
        return Response(response=ret,status=401,mimetype="application/json")
    try:
        friend = User.objects(id=friend).first()
        if friend:
            original = user
            if friend.id == original.id:
                raise
            original.friends.append(str(friend.id))
            friend.friends.append(str(original.id))
            original.save()
            friend.save()
            ret = '{"status":"Error","message":"Friend added successfully"}'
            return Response(response=ret,status=200,mimetype="application/json")
        else :
            raise
    except Exception as e:
        ret = '{"status":"Error","message":"Invalid Friend ID Specified"}'
        return Response(response=ret,status=500,mimetype="application/json")


def getFriendList():
    user = validateSession(request)
    if not user:
        ret = '{"status":"Fail","message":"Please login"}'
        return Response(response=ret,status=401,mimetype="application/json")
    try:
        friendList=[]
        if user.friends:
            for f in user.friends:
                u = {}
                t_user = User.objects(id=f).first()
                if t_user:
                    u['name']=t_user.name
                    u['email']=t_user.email
                    u['id']=t_user.id
                    friendList.append(u)
                    
        if friendList:
            ret = json.dumps(friendList)
            return Response(response=ret,status=200,mimetype="application/json")
        else:
            raise
    except Exception as e:
        ret = '{"status":"Error","message":"Could not find friends"}'
        return Response(response=ret,status=500,mimetype="application/json")
    

def forgotPassword(email):
    user = User.objects(email=email).first()
    if not user:
        return None
    else:
        return user


