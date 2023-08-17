from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse

class PrefixUrl(models.Model):
    title = models.CharField(max_length=128)
    url = models.CharField(max_length=256)
    icon_class = models.CharField(max_length=128)
    location = models.CharField(max_length=128)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.url

class User(models.Model):
    auth_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.CharField(max_length=128, verbose_name='email')
    first_name = models.CharField(max_length=128, verbose_name='first name')
    last_name = models.CharField(max_length=256, verbose_name='last name', null=True)
    pub_date = models.DateTimeField('date published', default=timezone.now)

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('update-user', kwargs={'pk': self.pk})

class Position(models.Model):
    auth_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, verbose_name='position name')
    pub_date = models.DateTimeField('date published', default=timezone.now)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('update-position', kwargs={'pk': self.pk})

class Segmentation(models.Model):
    auth_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, verbose_name='segmentation name')
    pub_date = models.DateTimeField('date published', default=timezone.now)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('update-segmentation', kwargs={'pk': self.pk})

class UserPosition(models.Model):
    auth_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published', default=timezone.now)

class UserSegmentation(models.Model):
    auth_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    segmentation = models.ForeignKey(Segmentation, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published', default=timezone.now)
