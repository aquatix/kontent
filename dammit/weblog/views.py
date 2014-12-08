from django.shortcuts import render
from django.http import HttpResponse
from .models import *

def home(request):
    return HttpResponse('You are home. Have a hot beverage.')


def post(request, postid):
    return HttpResponse('You are viewing a post.')


def archive(request, year=None):
    return HttpResponse('You are viewing the archive.')
