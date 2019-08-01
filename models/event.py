from models.base_model import BaseModel
from flask import flash
import peewee as pw
from playhouse.hybrid import hybrid_property
from config import S3_LOCATION, DEFAULT_EVENT_IMAGE
from datetime import datetime, timedelta

class Event(BaseModel):
    event_name = pw.CharField(null=False)
    description = pw.CharField(null=True)
    location = pw.CharField(default="TBC")
    host = pw.ForeignKeyField(User, backref='events_hosting')
    time = pw.DateTimeField(default = datetime.datetime.now)
    event_image = pw.CharField(default=DEFAULT_EVENT_IMAGE)
    guest = pw.ForeignKeyField(User, backref='events_attending')
    max_number=pw.IntegerField(default=0)
    private = pw.BooleanField(default = True)

    @hybrid_property
    def event_image_url(self):
        return S3_LOCATION + self.event_image
    
    def validate(self):
        #check that event has at least a name
        if self.event_name==''
            self.errors.append('Event name cannot be empty')
        
        #check that the event time is at least 1 minute in advance of current time. Might be an issue due to server lag / timeout.
        current_time=datetime.datetime.now()
        if (self.time -  current_time) < datetime.timedelta(minutes=1):
            self.errors.append('Event has to be in the future')
 