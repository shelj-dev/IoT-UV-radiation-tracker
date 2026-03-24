from django.db import models

class uv(models.Model):
    thereshold = models.IntegerField()

class sensor_data(models.Model):
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)