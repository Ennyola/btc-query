from django.db import models

# Create your models here.
class Price(models.Model):
    price = models.FloatField()