'''
Created on 05-Dec-2013

@author: blackpearl
'''

from threading import Thread
from flask.ext.mail import Message
from com.nc.medapp.controller.ApiEndPoints import mail

#@async    
def send_async_email(msg):
    mail.send(msg)
    
def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender = sender, recipients = recipients)
    msg.body = text_body
    msg.html = html_body
    #send_async_email(msg)
    thr = Thread(target = send_async_email, args = [msg])
    thr.start()
        