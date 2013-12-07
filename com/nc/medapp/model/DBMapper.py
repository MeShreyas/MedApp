'''
Created on 01-Dec-2013

@author: blackpearl
'''
from mongoengine import *

class Session(Document):
    user = StringField(required=True)
    token = StringField(required=True)
    createdTime =  DateTimeField()

class User(Document):
    name = StringField(required=True)
    email = EmailField(required=True)
    password = StringField(required=True)
    speciality = StringField(choices=('EAR','NOSE','THROAT'),required=True)
    friends = ListField(StringField())

    def clean(self):
        if self.speciality == 'EAR' :
            msg = "No Kan ka doctor dost"
            raise ValidationError(msg)

class Event(Document):
    # TODO: This is where I define my event data object
    pass


if __name__ == '__main__' :
    connect('test')
    data = User(name="Shreyas",email="This",password="password",speciality='NOSE')
    data.save()
    

