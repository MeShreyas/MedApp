'''
Created on 27-Jan-2014

@author: blackpearl
'''
import json
from flask import Flask
from flask import request,abort,render_template,Response
from com.nc.medapp.util.Helper import validateSession, validateJSON
from com.nc.medapp.model.DBMapper import Target, Goal
from mongoengine import *
import dateutil.parser


def setTargets():
    user = validateSession(request)
    if not user:
        ret = '{"status":"Fail","message":"Please login"}'
        return Response(response=ret,status=401,mimetype="application/json")
    validateJSON(request.json)
    targetDate = dateutil.parser.parse(request.json.get('startDate'));
    hours = request.json.get('hours');
    target = Target(user = user, startDate = targetDate, hours = hours)
    try:
        target.save()
    except Exception as e:
        ret = '{"status":"Fail","message":"Standard server errors"}'
        return Response(response=ret,status=401,mimetype="application/json")
    ret = '{"status":"Success","message":"Target has been set now","target":"'+str(target.id)+'"}'
    return Response(response=ret,status=200,mimetype="application/json")


def getTargets():
    user = validateSession(request)
    if not user:
        ret = '{"status":"Fail","message":"Please login"}'
        return Response(response=ret,status=401,mimetype="application/json")
    objs = Target.objects(user=user)
    temp_list=[]
    for obj in objs:
        response = {}
        response['startDate'] = obj.startDate.isoformat()
        response['hours'] = str(obj.hours)
        response['id'] = str(obj.id)
        goals =[]
        if obj.goals :            
            for goal in obj.goals:
                t_goal={}
                t_goal['desc'] = goal.goalDesc;
                t_goal['number'] = goal.goalNumber;
                goals.append(t_goal)
        if goals:
            response['goals']=goals
        temp_list.append(response)
    ret = json.dumps(temp_list)
    return Response(response=ret,status=200,mimetype="application/json")
        


def getTarget(target):
    user = validateSession(request)
    if not user:
        ret = '{"status":"Fail","message":"Please login"}'
        return Response(response=ret,status=401,mimetype="application/json")
    targetObj = Target.objects(id=target).first()
    if targetObj:
        response = {}
        response['startDate'] = targetObj.startDate.isoformat()
        response['hours'] = str(targetObj.hours)
        goals =[]
        if targetObj.goals :            
            for goal in targetObj.goals:
                t_goal={}
                t_goal['desc'] = goal.goalDesc;
                t_goal['number'] = goal.goalNumber;
                goals.append(t_goal)
        if goals:
            response['goals']=goals
    ret = json.dumps(response)
    return Response(response=ret,status=200,mimetype="application/json")

def setGoals(target):
    user = validateSession(request)
    if not user:
        ret = '{"status":"Fail","message":"Please login"}'
        return Response(response=ret,status=401,mimetype="application/json")
    validateJSON(request.json)
    goals = request.json.get('goals');
    goalList = []
    for goal in goals :
        g = Goal(goalNumber = goal['number'],goalDesc=goal['desc'])
        goalList.append(g)
    targetObj = Target.objects(id=target).first()
    targetObj.goals = goalList
    try :
        targetObj.save()
    except Exception as e:
        ret = '{"status":"Fail","message":"Standard server errors"}'
        return Response(response=ret,status=401,mimetype="application/json")
    ret = '{"status":"Success","message":"Goals have been set now"}'
    return Response(response=ret,status=200,mimetype="application/json")



