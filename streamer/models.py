from msilib.schema import Class
from re import X
from django.db import models
from django.forms import DurationField, model_to_dict
from datetime import timedelta

# Create your models here.
class Person(models.Model):
    en_id=models.CharField(primary_key=True,max_length=12)
    name=models.CharField(max_length=40)
    area=models.CharField(max_length=20)
    duration=models.DurationField(default=timedelta(seconds=0))
    face_encodes=models.BinaryField(default=b'')

    def __str__(self):
        return self.name

    