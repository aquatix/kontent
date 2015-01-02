from django.contrib import admin
from django.db import models
from django.contrib.sites.models import Site
from .models import (
        SiteUser,
        SiteConfig,
        Tag,
        Comment,
        ContentGroup,
        Article,
        Link,
        Image,
        Binary)


class SiteUserAdmin(admin.ModelAdmin):
    #list_display = ('user', 'user__first_name', 'user__last_name', 'website',)
    list_display = ('user', 'website',)
    search_fields = ['user', 'website']


class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ('site',)
    #search_fields = ['name', 'domain']


class ContentGroupAdmin(admin.ModelAdmin):
    #list_display = ('name', 'parent')
    #list_display = ('site')
    list_display = ('title',)


class ContentItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published', 'public', 'publish_from', 'publish_to')


class TagAdmin(admin.ModelAdmin):
    list_display = ('tag', 'slug')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'siteuser', 'name', 'email_address', 'ip',)


class ImageAdmin(admin.ModelAdmin):
    search_fields = ['title']


admin.site.register(SiteUser, SiteUserAdmin)
admin.site.register(SiteConfig, SiteConfigAdmin)
admin.site.register(ContentGroup, ContentGroupAdmin)
admin.site.register(Article, ContentItemAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
