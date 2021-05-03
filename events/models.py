from django.db import models

class Rooms(models.Model):
    name = models.CharField(max_length=15)

class Events(models.Model):
    room = models.ForeignKey(Rooms)
    summary = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

class Users(models.Model):
    username = models.CharField(max_length=20)

class EventUserMappings(models.Model):
    event = models.ForeignKey(Events)
    user = models.ForeignKey(Users)