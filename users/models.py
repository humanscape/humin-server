from django.db import models

class Users(models.Model):
    email = models.CharField(max_length=100)
