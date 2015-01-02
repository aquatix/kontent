from django.contrib.sites.shortcuts import get_current_site
from django.template import Context, Template
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from datetime import date
from django.contrib.sites.models import Site
from .models import *


def load_template(request, site, template, context):
    """
    Looks for the template in the default place or use a custom theme set in the SiteConfig
    """
    siteconfig = SiteConfig.objects.get(site=site)
    if siteconfig.template:
        # A custom theme is defined
        with open (siteconfig.template + '/templates/' + template, "r") as myfile:
            templatefile = myfile.read().replace('\n', '')
        customtemplate = Template(templatefile)
        c = Context(context)
        return customtemplate.render(c)
    # Use the default template
    return render(request, settings.TEMPLATE_DIR + template, context)


def home(request):
    """
    Homepage
    /
    """
    site = get_current_site(request)
    articles = Article.objects.filter(publish_from__year=date.today().year, public=True, sites__id=site.id)
    return load_template(request, site, 'home_overview.html', {'articles': articles})


def article(request, article_id):
    """
    Article detail view
    /p/<id>/
    """
    site = get_current_site(request)
    article = get_object_or_404(Article, pk=article_id, sites__id=site.id)
    return load_template(request, site, 'article.html', {'article': article})


def article_archive(request, year=None):
    """
    Article archive
    /archive/
    """
    site = get_current_site(request)
    if year:
        articles = Article.objects.filter(publish_from__year=str(year), public=True, sites__id=site.id)
    else:
        articles = Article.objects.filter(publish_from__year=date.today().year, public=True, sites__id=site.id)
    return load_template(request, site, 'archive.html', {'articles': articles})


def link_archive(request, year=None):
    """
    Link (blogmark) archive
    /m/
    """
    site = get_current_site(request)
    links = Link.objects.filter(publish_from__year=year, public=True, sites__id=site.id)
    return load_template(request, site, 'link_archive.html', {'links': links})


def link(request, item_id):
    """
    Link (blogmark)
    /m/<id>/
    """
    site = get_current_site(request)
    link = get_object_or_404(Link, pk=item_id, sites__id=site.id)
    return load_template(request, site, 'link.html', {'link': link})
