from django.db import models
class Room(models.Model):
    name = models.CharField(max_length=15)
    calendar_id = models.CharField(max_length=100, null=True)

class Event(models.Model):
    room = models.ForeignKey(Room, on_delete=models.DO_NOTHING, related_name='events')
    summary = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

class Users(models.Model):
    username = models.CharField(max_length=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, related_name='users')