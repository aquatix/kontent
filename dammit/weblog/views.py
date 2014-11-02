from django.shortcuts import render
from django.http import HttpResponse
from .models import *

def home(request):
    return HttpResponse('You are home. Have a hot beverage.')
