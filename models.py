from django.db.models import Model, CharField, IntegerField, DateTimeField, ForeignKey, CASCADE
from django.conf import settings
from django.urls import reverse

class NavLink(Model):
    title = CharField('title', max_length=128)
    path = CharField('full path', max_length=256)
    icon_class = CharField('bootstrap icon', max_length=128)
    date_created = DateTimeField('date created', auto_now_add=True)

    def __str__(self):
        return self.path

class User(Model):
    auth_user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, verbose_name='who submitted')
    email = CharField('email', max_length=128)
    first_name = CharField('first name', max_length=128)
    last_name = CharField('last name', max_length=256, null=True)
    pub_date = DateTimeField('date published', auto_now_add=True)

    def __str__(self):
        return self.email

    def get_absolute_url(self, view_name=None):
        view_name = view_name if view_name is not None else self.view_name

        if view_name is not None:
            return reverse(view_name, kwargs={'pk': self.pk})

        return None

    def get_full_name(self):
        if self.last_name is not None:
            return '%s %s' % (self.first_name, self.last_name)

        return self.first_name

class Position(Model):
    auth_user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, verbose_name='who submitted')
    name = CharField('position name', max_length=128)
    date_created = DateTimeField('date created', auto_now_add=True)
    date_updated = DateTimeField('date updated', auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self, view_name=None):
        view_name = view_name if view_name is not None else self.view_name

        if view_name is not None:
            return reverse(view_name, kwargs={'pk': self.pk})

        return None

class Segmentation(Model):
    auth_user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, verbose_name='who submitted')
    name = CharField('segmentation name', max_length=128)
    date_created = DateTimeField('date created', auto_now_add=True)
    date_updated = DateTimeField('date updated', auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self, view_name=None):
        view_name = view_name if view_name is not None else self.view_name

        if view_name is not None:
            return reverse(view_name, kwargs={'pk': self.pk})

        return None

class UserPosition(Model):
    auth_user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, verbose_name='who submitted')
    user = ForeignKey(User, on_delete=CASCADE, verbose_name='email')
    position = ForeignKey(Position, on_delete=CASCADE, verbose_name='position name')
    date_created = DateTimeField('date created', auto_now_add=True)
    date_updated = DateTimeField('date updated', auto_now=True)

class UserSegmentation(Model):
    auth_user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, verbose_name='who submitted')
    user = ForeignKey(User, on_delete=CASCADE, verbose_name='email')
    segmentation = ForeignKey(Segmentation, on_delete=CASCADE, verbose_name='segmentation name')
    date_created = DateTimeField('date created', auto_now_add=True)
    date_updated = DateTimeField('date updated', auto_now=True)
