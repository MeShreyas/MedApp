'''
Created on 01-Dec-2013

@author: blackpearl
'''
from mongoengine import *
import datetime

class Speciality(Document):
    fieldname = StringField(required=True)
    
class Country(Document):
    name = StringField(required=True)

class User(Document):
    name = StringField(required=True)
    email = EmailField(required=True,unique=True)
    password = StringField(required=True)
    speciality = ReferenceField(Speciality,required=True)
    country = ReferenceField(Country, required=False)
    friends = ListField(StringField())
    enabled = BooleanField(default=False,required=True)
    created = DateTimeField(default=datetime.datetime.now())

    def clean(self):
        if self.speciality == 'EAR' :
            msg = "No Kan ka doctor dost"
            raise ValidationError(msg)

class Token(Document):
    user = ReferenceField(User,required=True)
    token = StringField(required=True)

class Session(Document):
    user = ReferenceField(User)
    created =  DateTimeField(default=datetime.datetime.now())

class Goal(EmbeddedDocument):
    goalNumber = IntField(required=True)
    goalDesc = StringField(required=True)
    

class Target(Document):
    user = ReferenceField(User)
    startDate = DateTimeField(required=True)
    hours = DecimalField(required=True)
    goals = ListField(EmbeddedDocumentField(Goal))

class Eventtype(Document):
    eventType = StringField(required=True)

class Event(Document):
    user = ReferenceField(User)
    startDate = DateTimeField(required=True)
    endDate = DateTimeField(required=True)
    eventType = ReferenceField(Eventtype,required=True)
    title = StringField(required=True)
    hours = DecimalField(required=True)
    photos = ListField()
    notes = StringField()
    status = StringField()
    


