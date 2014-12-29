from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from datetime import date
from django.contrib.sites.models import Site
from .models import *


def home(request):
    """
    Homepage
    /
    """
    articles = Article.objects.filter(publish_from__year=date.today().year, public=True, sites__id=get_current_site(request).id)
    return render(request, settings.TEMPLATE_DIR + 'home_overview.html', {'articles': articles})
    #return HttpResponse('You are home. Have a hot beverage.')


def article(request, article_id):
    """
    Article detail view
    /p/<id>/
    """
    article = get_object_or_404(Article, pk=article_id, sites__id=get_current_site(request).id)
    return render(request, settings.TEMPLATE_DIR + 'article.html', {'article': article})


def article_archive(request, year=None):
    """
    Article archive
    /archive/
    """
    if year:
        articles = Article.objects.filter(publish_from__year=str(year), public=True, sites__id=get_current_site(request).id)
    else:
        articles = Article.objects.filter(publish_from__year=date.today().year, public=True, sites__id=get_current_site(request).id)
    return render(request, settings.TEMPLATE_DIR + 'archive.html', {'articles': articles})
    #return HttpResponse('You are viewing the archive (year: {0}).'.format(year))


def link_archive(request, year=None):
    """
    Link (blogmark) archive
    /m/
    """
    links = Link.objects.filter(publish_from__year=year, public=True, sites__id=get_current_site(request).id)
    return render(request, settings.TEMPLATE_DIR + 'link_archive.html', {'links': links})
    #return HttpResponse('You are viewing the link archive (year: {0}).'.format(year))


def link(request, item_id):
    """
    Link (blogmark)
    /m/<id>/
    """
    link = get_object_or_404(Link, pk=item_id, sites__id=get_current_site(request).id)
    return render(request, settings.TEMPLATE_DIR + 'link.html', {'link': link})
