'''
Created on 01-Dec-2013

@author: blackpearl
'''
from mongoengine import *
import datetime

class Speciality(Document):
    fieldname = StringField(required=True)

class User(Document):
    name = StringField(required=True)
    email = EmailField(required=True)
    password = StringField(required=True)
    speciality = ReferenceField(Speciality,required=True)
    friends = ListField(StringField())
    enabled = BooleanField(default=False,required=True)
    created = DateTimeField(default=datetime.datetime.now())

    def clean(self):
        if self.speciality == 'EAR' :
            msg = "No Kan ka doctor dost"
            raise ValidationError(msg)


class Session(Document):
    user = ReferenceField(User)
    created =  DateTimeField(default=datetime.datetime.now())

class Event(Document):
    # TODO: This is where I define my event data object
    pass


if __name__ == '__main__' :
    connect('test')
    data = User(name="Shreyas",email="This",password="password",speciality='NOSE')
    data.save()
    

