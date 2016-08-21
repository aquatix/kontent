from django.conf.urls import include, url
from django.contrib import admin

    # Examples:
    # url(r'^$', 'kontentsite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

admin.autodiscover()

urlpatterns = [
    url(r'^', include('kontent.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
