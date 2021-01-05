from django.db import models

# Create your models here.

import datetime


class CookieConsent(models.Model):
    user = models.CharField(max_length=64)
    sessn = models.CharField(max_length=64)
    concent = models.BooleanField(default=False)
    last_modified = models.DateField(default=datetime.date.today)
