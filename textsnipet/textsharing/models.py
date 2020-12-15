from django.db import models


import datetime


# Create your models here.

class TextInfo(models.Model):
    text = models.TextField()
    hash = models.CharField(max_length=32)
    isEnc = models.BooleanField(default=False)
    enc_key =models.CharField(max_length=32)
    last_modified = models.DateField(default=datetime.date.today)


    # def get_random_string(self,length):
    #     # Random string with the combination of lower and upper case
    #     letters = string.ascii_letters
    #     result_str = ''.join(secrets.choice(letters) for i in range(length))
    #     return result_str


