from django.db import models

class User(models.Model):

    ORGANIZATION_TYPE = (
        (0, 'NONE'),
        (1, 'HUMANSCAPE'),
        (2, 'MOMMYTALK')
    )

    email = models.CharField(max_length=100)
    name = models.CharField(max_length=20, null=True)
    # human = 1, mommy = 2
    organization = models.IntegerField(default=0, choices=ORGANIZATION_TYPE)