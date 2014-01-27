'''
Created on 28-Jan-2014

@author: blackpearl
'''

import json
from flask import Flask
from flask import request,abort,render_template,Response
from com.nc.medapp.util.Helper import validateJSON, validateSession
import dateutil.parser
from com.nc.medapp.exception.ValueError import MedAppValueError
from com.nc.medapp.model.DBMapper import Eventtype, Event


def createEvent():
    validateJSON(request.json)
    user = validateSession(request)
    if not user:
        ret = '{"status":"Fail","message":"Please login"}'
        return Response(response=ret,status=401,mimetype="application/json")
    
    try:        
        startDate = dateutil.parser.parse(request.json.get('startDate'))
        if not startDate:
            raise MedAppValueError('StartDate is required')
        endDate = dateutil.parser.parse(request.json.get('endDate'))
        if not endDate:
            raise MedAppValueError('EndDate is required')
        eventType = request.json.get('eventType')
        if not eventType:
            raise MedAppValueError('EventType is required')
        title = request.json.get('title')
        if not title:
            raise MedAppValueError('Title is required')
        hours = request.json.get('hours')
        if not hours:
            raise MedAppValueError('Hours is required')
        notes = request.json.get('notes')
        if not notes :
            notes = ''
        # Fetch the event type object
        eventTypeObj = Eventtype.objects(eventType=eventType).first()
        if not eventTypeObj:
            raise MedAppValueError('Invalid event type')
        
        event = Event(user=user,startDate=startDate,endDate=endDate,eventType=eventTypeObj,title=title,hours=hours,notes=notes)
        event.save()
        ret = '{"status":"Success","message":"Event has been created","eventId":"'+str(event.id)+'"}'
        return Response(response=ret,status=200,mimetype="application/json")
    except MedAppValueError as e :
        ret = '{"status":"Fail","message":"'+str(e)+'"}'
        resp = Response(response=ret,status=500,mimetype="application/json")
        return resp
    except Exception as e:
        ret = '{"status":"Fail","message":"Failed to create event '+str(e)+'"}'
        resp = Response(response=ret,status=500,mimetype="application/json")
        return resp
    

def getEvents():
    user = validateSession(request)  
    if not user:
        ret = '{"status":"Fail","message":"Please login"}'
        return Response(response=ret,status=401,mimetype="application/json")

    events = Event.objects
    temp_list=[]
    for event in events:
        temp_eve = {}
        temp_eve['name'] = event.title
        temp_eve['id'] = str(event.id)
        temp_eve['startDate'] = event.startDate.isoformat()
        temp_eve['endDate'] = event.endDate.isoformat()
        temp_eve['hours']=str(event.hours)
        temp_list.append(temp_eve)
    return json.dumps(temp_list) 

def updateEvent(eventId):
    validateJSON(request.json)
    user = validateSession(request)
    if not user:
        ret = '{"status":"Fail","message":"Please login"}'
        return Response(response=ret,status=401,mimetype="application/json")
    
    try:
        # Fetch the event based on id
        if not eventId:
            ret = '{"status":"Fail","message":"No Event Id Specified"}'
            return Response(response=ret,status=500,mimetype="application/json")
        
        try:
            event = Event.objects(id=eventId).first()
            if not event:
                raise
        except Exception as e:
            ret = '{"status":"Fail","message":"Invalid Event Id Specified"}'
            return Response(response=ret,status=500,mimetype="application/json")
                
        if request.json.get('startDate'):
            startDate = dateutil.parser.parse(request.json.get('startDate'))
            if startDate:
                event.startDate = startDate
        if request.json.get('endDate'):
            endDate = dateutil.parser.parse(request.json.get('endDate'))
            if endDate:
                event.endDate = endDate
        eventType = request.json.get('eventType')
        if eventType:
            eventTypeObj = Eventtype.objects(eventType=eventType).first()
            if not eventTypeObj:
                raise MedAppValueError('Invalid event type')
            event.eventType = eventTypeObj
        title = request.json.get('title')        
        if title:
            event.title = title
        hours = request.json.get('hours')
        if hours:
            event.hours = hours
        notes = request.json.get('notes')
        if notes:
            event.notes = event.notes+"||"+notes
            
        event.save()
        ret = '{"status":"Success","message":"Event has been updated","eventId":"'+str(event.id)+'"}'
        return Response(response=ret,status=200,mimetype="application/json")
    except MedAppValueError as e :
        ret = '{"status":"Fail","message":"'+str(e)+'"}'
        resp = Response(response=ret,status=500,mimetype="application/json")
        return resp
    except Exception as e:
        ret = '{"status":"Fail","message":"Failed to update event '+str(e)+'"}'
        resp = Response(response=ret,status=500,mimetype="application/json")
        return resp


def getEvent(eventId):
    user = validateSession(request)
    if not user:
        ret = '{"status":"Fail","message":"Please login"}'
        return Response(response=ret,status=401,mimetype="application/json")
    

    # Fetch the event based on id
    if not eventId:
        ret = '{"status":"Fail","message":"No Event Id Specified"}'
        return Response(response=ret,status=500,mimetype="application/json")
    
    try:
        event = Event.objects(id=eventId).first()
        if not event:
            raise
    except Exception as e:
        ret = '{"status":"Fail","message":"Invalid Event Id Specified"}'
        return Response(response=ret,status=500,mimetype="application/json")
    
    temp_eve = {}
    temp_eve['name'] = event.title
    temp_eve['id'] = str(event.id)
    temp_eve['startDate'] = event.startDate.isoformat()
    temp_eve['endDate'] = event.endDate.isoformat()
    temp_eve['hours']=str(event.hours)
    temp_eve['photos'] = []
    temp_eve['notes'] = event.notes
    for photo in event.photos:
        temp_eve['photos'].append(str(request.host_url)+"images/"+photo)
    
    return json.dumps(temp_eve)


if __name__ == '__main__':
    pass




