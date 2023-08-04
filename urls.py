from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('segmentations', views.segmentation, name='segmentations'),
    path('roles', views.role, name='roles'),
    path('users', views.user, name='users'),
]
