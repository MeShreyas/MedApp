'''
Created on 27-Jan-2014

@author: blackpearl
'''
from flask import Flask
from flask import request,abort,render_template,Response
from flask.ext.mail import Mail
from flask.ext.mail import Message
import random
import string
from com.nc.medapp.model.DBMapper import Token



# Helper methods
def validateSession(request):
    appToken = request.headers.get('appToken')
    if not appToken:
        return None
    token = Token.objects(token=appToken).first()
    if token and token.user:
        return token.user
    else:
        return None

def validateJSON(json):
    if not json:
        abort(401)



def generateToken():
    return ''.join(random.choice(string.ascii_uppercase) for i in range(12))
 
if __name__ == '__main__':
    pass