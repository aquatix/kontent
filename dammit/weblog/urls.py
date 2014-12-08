from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^p/(?P<postid>[0-9]+)$', views.post, name='post-detail'),
    url(r'^archive/(?P<year>[0-9]{4})/$', views.archive, name='archive-year'),
    url(r'^archive/$', views.archive, name='archive-year'),
]
