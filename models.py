from django.db import models

class User(models.Model):
    email = models.CharField(max_length=128)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=256)
    pub_date = models.DateTimeField('date published')

class Position(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    pub_date = models.DateTimeField('date published')

class Segmentation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    pub_date = models.DateTimeField('date published')

class UserPosition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')

class UserSegmentation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    segmentation = models.ForeignKey(Segmentation, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')
