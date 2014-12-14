from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import *

def home(request):
    return HttpResponse('You are home. Have a hot beverage.')


def article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render(request, settings.TEMPLATE_DIR + 'article.html', {'article': article})


def archive(request, year=None):
    #return render(request, settings.TEMPLATE_DIR + 'archive.html', {'article': article})
    return HttpResponse('You are viewing the archive (year: {0}).'.format(year))
