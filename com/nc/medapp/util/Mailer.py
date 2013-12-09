'''
Created on 05-Dec-2013

@author: blackpearl
'''

from threading import Thread
from flask.ext.mail import Message

class Mailer():
    
    mail = None

    def __init__(self,mail):
        self.mail = mail
        #self.sender  = sender 
        #self.recipients = recipients
        
    def send_email(self,subject,  recipients, text_body, html_body):
    
        sender= "patilshreyas27@gmail.com";
        recipients = ["waghman@gmail.com","simplychampak@gmail.com"]
        msg = Message(subject, sender = sender, recipients = recipients)
        msg.body = text_body
        msg.html = html_body
        def send_async_email(msg):
             self.mail.send(msg)
        thr = Thread(target = send_async_email, args = [msg])
        thr.start()
