from django.db import models
from django.db.models.deletion import CASCADE

class Rooms(models.Model):
    name = models.CharField(max_length=15)

class Events(models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.DO_NOTHING)
    summary = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    users = models.ManyToManyField('Users', through='EventUserMappings')

class Users(models.Model):
    username = models.CharField(max_length=20)

class EventUserMappings(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=CASCADE)