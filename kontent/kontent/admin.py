"""
Django admin stuff for the kontent framework
"""
from django.contrib import admin
#from django.contrib.sites.models import Site
from .models import (\
        SiteUser,
        SiteConfig,
        Tag,
        Comment,
        ContentGroup,
        Article,
        Page,
        Link,
        Image,
        Binary,
        Redirect)


class SiteUserAdmin(admin.ModelAdmin):
    """
    Modify users registered in kontent
    """
    #list_display = ('user', 'user__first_name', 'user__last_name', 'website',)
    list_display = ('user', 'website',)
    search_fields = ['user', 'website']


class SiteConfigAdmin(admin.ModelAdmin):
    """
    Modify site-specific configuration, like the name and domain
    """
    list_display = ('site',)
    #search_fields = ['name', 'domain']


class ContentGroupAdmin(admin.ModelAdmin):
    #list_display = ('name', 'parent')
    #list_display = ('site')
    list_display = ('title',)


class ContentItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published', 'public', 'publish_from', 'publish_to')


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'public',)


class TagAdmin(admin.ModelAdmin):
    """
    Add and modify tags used for labelling content
    """
    list_display = ('tag', 'slug')


class CommentAdmin(admin.ModelAdmin):
    """
    Admin for the comments on content
    """
    list_display = ('content_object', 'siteuser', 'name', 'email_address', 'ip_address',)


class ImageAdmin(admin.ModelAdmin):
    """
    Admin for image objects
    """
    search_fields = ['title']


class BinaryAdmin(admin.ModelAdmin):
    search_fields = ['title']


class LinkAdmin(admin.ModelAdmin):
    search_fields = ['title']


class RedirectAdmin(admin.ModelAdmin):
    search_fields = ['match', 'target_uri']


admin.site.register(SiteUser, SiteUserAdmin)
admin.site.register(SiteConfig, SiteConfigAdmin)
admin.site.register(ContentGroup, ContentGroupAdmin)
admin.site.register(Article, ContentItemAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Binary, BinaryAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Redirect, RedirectAdmin)
