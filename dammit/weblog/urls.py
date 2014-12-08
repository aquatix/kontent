from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^/p/([0-9]{4})/$', views.post, name='post-detail'),
    url(r'^/archive/([0-9]{4})/$', views.archive, name='archive-year'),
]
