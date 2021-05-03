from django.db import models
class Rooms(models.Model):
    name = models.CharField(max_length=15)
    calendar_id = models.CharField(max_length=100, null=True)

class Events(models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.DO_NOTHING)
    summary = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

class Users(models.Model):
    username = models.CharField(max_length=100)
    event = models.ForeignKey(Events, on_delete=models.CASCADE, null=True)