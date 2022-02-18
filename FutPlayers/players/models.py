from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    position = models.CharField(max_length=50)
    nation = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
