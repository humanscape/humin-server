from django.db import models

class Users(models.Model):
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=20, null=True)
    # human = 1, mommy = 2
    organization = models.IntegerField(default=0)