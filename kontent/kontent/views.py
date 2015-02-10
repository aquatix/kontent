"""
Views for kontent framework
"""
from django.contrib.sites.shortcuts import get_current_site
#from django.template import Context, Template
from django.shortcuts import render
#from django.utils.translation import ugettext as _
#from django.http import HttpResponse
from django.shortcuts import get_object_or_404
#from django.contrib.sites.models import Site
from django.conf import settings
from datetime import date, datetime
import os
from .models import (\
        SiteConfig,
        Article,
        Link)

"""
class SiteMixin(object):
  def get_site(self):
    return get_current_site(request)

  def get_context_data(self, **kwargs):
    ctx = super(SiteMixin, self).get_context_data(**kwargs)
    ctx['site'] = self.get_site()
    return ctx
"""

def load_template(request, site, template, context):
    """
    Looks for the template in the default place or use a custom theme set in the SiteConfig
    """
    siteconfig = SiteConfig.objects.get(site=site)
    if siteconfig.template:
        # A custom theme is defined
        template_dir = os.path.join(siteconfig.template, 'templates/')
    else:
        # Use the default template
        template_dir = settings.TEMPLATE_DIR
    #print(template_dir)
    #print(template_dir + template)
    context['template_dir'] = template_dir
    context['site'] = site
    context['siteconfig'] = siteconfig
    context['current_year'] = datetime.now().year
    context['base_template'] = os.path.join(template_dir, 'base_generic.html')
    return render(request, os.path.join(template_dir, template), context)


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
    this_article = get_object_or_404(Article, pk=article_id, sites__id=site.id)
    previous_article = this_article.previous_item(site)
    next_article = this_article.next_item(site)
    print(previous_article)
    print(next_article)
    return load_template(request, site, 'article_page.html', \
            {'article': this_article, 'previous_article': previous_article, 'next_article': next_article})


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
    this_link = get_object_or_404(Link, pk=item_id, sites__id=site.id)
    return load_template(request, site, 'link.html', {'link': this_link})


def page(request, page_slug):
    """
    Content page
    """
    site = get_current_site(request)
    this_page = get_object_or_404(Page, slug=page_slug, sites__id=site.id)
    return load_template(request, site, 'page.html', {'page': this_page})


def about(request):
    """
    Special case: about page
    """
    return page(request, 'about')
