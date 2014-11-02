from django.contrib import admin
from django.db import models
from .models import (
        SiteUser,
        Site,
        Tag,
        ContentGroup,
        ContentItem)


class SiteUserAdmin(admin.ModelAdmin):
    #list_display = ('user', 'user__first_name', 'user__last_name', 'website',)
    list_display = ('user', 'website',)
    search_fields = ['user', 'website']


class SiteAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ['title']


class ContentGroupAdmin(admin.ModelAdmin):
    #list_display = ('name', 'parent')
    #list_display = ('site')
    list_display = ('title',)


class ContentItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published', 'public', 'publish_from', 'publish_to')


class TagAdmin(admin.ModelAdmin):
    list_display = ('tag', 'slug')


admin.site.register(SiteUser, SiteUserAdmin)
admin.site.register(Site, SiteAdmin)
admin.site.register(ContentGroup, ContentGroupAdmin)
admin.site.register(ContentItem, ContentItemAdmin)
admin.site.register(Tag, TagAdmin)
