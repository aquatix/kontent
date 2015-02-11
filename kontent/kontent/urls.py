"""
url configuration of the kontent CMS
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^p/about/$', views.about, name='about'),
    url(r'^p/(?P<article_id>[0-9]+)$', views.article, name='article-detail'),
    url(r'^archive/(?P<year>[0-9]{4})/$', views.article_archive, name='article_archive-year'),
    url(r'^archive/$', views.article_archive, name='article_archive-list'),
    url(r'^m/(?P<year>[0-9]{4})/$', views.link_archive, name='link_archive-year'),
    url(r'^m/$', views.link_archive, name='link_archive-list'),
    url(r'^search/', views.search, name='search'),
    url(r'^feed/', views.rss_feed, name='feed'),
]
