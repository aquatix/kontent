from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from datetime import date
from .models import *

def home(request):
    articles = Article.objects.filter(publish_from__year=date.today().year, public=True)
    return render(request, settings.TEMPLATE_DIR + 'home_overview.html', {'articles': articles})
    #return HttpResponse('You are home. Have a hot beverage.')


def article(request, article_id):
    article = get_object_or_404(Article, pk=article_id, sites__id=get_current_site(request).id)
    return render(request, settings.TEMPLATE_DIR + 'article.html', {'article': article})


def article_archive(request, year=None):
    if year:
        articles = Article.objects.filter(publish_from__year=str(year), public=True)
    else:
        articles = Article.objects.filter(publish_from__year=date.today().year, public=True)
    return render(request, settings.TEMPLATE_DIR + 'archive.html', {'articles': articles})
    #return HttpResponse('You are viewing the archive (year: {0}).'.format(year))


def link_archive(request, year=None):
    articles = Link.objects.filter(publish_from__year=year, public=True)
    return render(request, settings.TEMPLATE_DIR + 'link_archive.html', {'links': links})
    #return HttpResponse('You are viewing the link archive (year: {0}).'.format(year))


def link(request, item_id):
    link = get_object_or_404(link, pk=item_id)
    return render(request, settings.TEMPLATE_DIR + 'link.html', {'link': link})
