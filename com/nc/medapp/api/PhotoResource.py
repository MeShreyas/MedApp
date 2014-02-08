'''
Created on 28-Jan-2014

@author: blackpearl
'''

import os
from flask import Flask
from flask import request,abort,render_template,Response
from com.nc.medapp.util.Helper import validateSession, generateToken
from com.nc.medapp.model.DBMapper import Event


UPLOADS_FOLDER='/MedApp/images'


def uploadPhoto(eventId):
    photos = []
    accessUrl = ""
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
            photos = event.photos
            if not photos:
                photos=[]
        except Exception as e:
            ret = '{"status":"Fail","message":"Invalid Event Id Specified"}'
            return Response(response=ret,status=500,mimetype="application/json")
        
        if request.method == 'POST' and request.data:
            file = request.data;
            filetype = file[file.index('/')+1:file.index(';base64,')]
            file=file[file.index(',')+1:]
            userid = str(user.id)
            filename=userid[:5]+generateToken()+"."+filetype
            fh = open(UPLOADS_FOLDER+os.sep+filename, "wb")
            fh.write(file.decode('base64'))
            fh.close()
            event.photos.append(filename)
            event.save()
            accessUrl = str(request.host_url)+"images/"+filename
        else:
            raise 
        
    except Exception as e:
        ret = '{"status":"Fail","message":"Failed to upload photo"}'
        resp = Response(response=ret,status=500,mimetype="application/json")
        return resp
        
    ret = '{"status":"Success","message":"Image Upload Complete","url":"'+accessUrl+'"}'
    return Response(response=ret,status=200,mimetype="application/json")

if __name__ == '__main__':
    pass
