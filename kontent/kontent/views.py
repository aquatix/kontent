"""
Views for kontent framework
"""
from django.contrib.sites.shortcuts import get_current_site
#from django.template import Context, Template
from django.shortcuts import render
#from django.utils.translation import ugettext as _
#from django.http import HttpResponse
#from django.views.generic import TemplateView, RedirectView
from django.views import generic
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView
#from django.contrib.sites.models import Site
from django.conf import settings
from datetime import date, datetime
import os
from .models import (\
        SiteConfig,
        Article,
        Page,
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
    context['search_key'] = '' # @TODO: text the visitor is searching on

    # Get siteconfig.nr_blogmarks_sidebar amount of blogmarks to show in the sidebar
    context['blogmarks'] = Link.objects.filter(public=True, sites__id=site.id)[:siteconfig.nr_blogmarks_sidebar]
    return render(request, os.path.join(template_dir, template), context)


#class DisplayGenericView(generic.TemplateView):
#
#    def get_context_data(self, kwargs):
#        context = super(DisplayGenericView, self).get_context_data(kwargs)
#        site = get_current_site(request)
#        siteconfig = SiteConfig.objects.get(site=site)
#        if siteconfig.template:
#            # A custom theme is defined
#            template_dir = os.path.join(siteconfig.template, 'templates/')
#        else:
#            # Use the default template
#            template_dir = settings.TEMPLATE_DIR
#        #print(template_dir)
#        #print(template_dir + template)
#        context['template_dir'] = template_dir
#        context['site'] = site
#        context['siteconfig'] = siteconfig
#        context['current_year'] = datetime.now().year
#        context['base_template'] = os.path.join(template_dir, 'base_generic.html')
#        context['search_key'] = '' # @TODO: text the visitor is searching on
#
#        # Get siteconfig.nr_blogmarks_sidebar amount of blogmarks to show in the sidebar
#        context['blogmarks'] = Link.objects.filter(public=True, sites__id=site.id)[:siteconfig.nr_blogmarks_sidebar]
#        return context
#        #return render(request, os.path.join(template_dir, template), context)


def home(request):
    """
    Homepage
    /
    """
    site = get_current_site(request)
    articles = Article.objects.filter(public=True, sites__id=site.id)
    return load_template(request, site, 'home_overview.html', {'articles': articles})


def article(request, slug):
    """
    Article detail view
    /p/slug
    """
    site = get_current_site(request)
    #this_article = get_object_or_404(Article, pk=article_id, sites__id=site.id)
    this_article = get_object_or_404(Article, slug=slug, sites__id=site.id)
    previous_article = this_article.previous_item(site)
    next_article = this_article.next_item(site)
    print(previous_article)
    print(next_article)
    return load_template(request, site, 'article_page.html', \
            {'article': this_article, 'previous_article': previous_article, 'next_article': next_article})


def article_short_id(request, short_id):
    site = get_current_site(request)
    this_article = get_object_or_404(Article, pk=article_id, sites__id=site.id)
    #blah


class DisplayArticleView(generic.TemplateView):
    template_name = "article_page.html"

    #def get_context_data(self, kwargs):
    #    print(kwargs)
    #    context = super(DisplayArticleView, self).get_context_data(kwargs)
    #    #context['article'] = Article.objects.get(slug=self.kwargs.get('article_slug', None))
    #    context['article'] = Article.objects.get(slug='blah')
    #    #context['article'] = Article.objects.get(slug=slug)
    #    return context


class DisplayArticleRedirectView(generic.RedirectView):

    def get(self, request, args, **kwargs):
        short_id = self.kwargs.get('short_id', None)
        article = Article.objects.get(short_id=short_id)
        self.url = '/p/%s-%s' % (article.id, article.slug)
        return super(DisplayArticleRedirectView, self).get(request, args, **kwargs)


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
    if not year:
        year = date.today().year
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


def search(request):
    """
    Search page
    """
    # @TODO: implement
    return 'search'


def rss_feed(request):
    """
    Generate an rss feed with articles
    """
    site = get_current_site(request)
    articles = Article.objects.filter(sites__id=site.id).order_by('-published_date')[20:]
    return load_template(request, site, 'rss_articles.html', {'articles': articles})
