from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse('OK')

def segmentation(request):
    return HttpResponse('SEGMENTATIONS')

def role(request):
    return HttpResponse('ROLES')

def user(request):
    return HttpResponse('USERS')
