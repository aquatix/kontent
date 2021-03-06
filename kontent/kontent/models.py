"""
The models used by the kontent framework
"""
from django.db import models
from django.db.models import Q
from django.db.models import Count
from django.db.models import signals
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from datetime import datetime
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.conf import settings
from hashids import Hashids


def update_short_id(sender, instance, created, **kwargs):
    if not instance.short_id:
        instance.short_id = instance.generate_short_id()


class BaseModel(models.Model):
    """
    Base model with common properties.
    """
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
        ordering = ('-date_created', )

    def __unicode__(self):
        return 'BaseModel created at {0}'.format(self.date_created)


class SiteUser(BaseModel):
    """
    User object, like a site admin, editor or authenticated visitor.
    """
    user = models.OneToOneField(User, related_name='authuser')
    website = models.CharField(max_length=255, blank=True, help_text='Optional, website/homepage of this user')

    @property
    def name(self):
        """
        Get a friendly name of this user
        """
        if not self.user.first_name and not self.user.last_name:
            return self.user.username
        else:
            return self.user.first_name + ' ' + self.user.last_name

    @classmethod
    def is_member(cls, user, groupname):
        """
        Check if user `user` is in group `groupname`
        """
        return user.groups.filter(name=groupname).exists()

    def __unicode__(self):
        if not self.user.first_name and not self.user.last_name:
            return self.user.username
        else:
            return '{0} [{1}]'.format(self.user.first_name, self.user)


class SiteConfig(BaseModel):
    """
    Site-specific configuration.
    """
    site = models.OneToOneField(Site)

    # Custom theme, directory
    template = models.CharField(max_length=255, blank=True)

    description = models.CharField(max_length=255, blank=True)
    startyear = models.IntegerField(blank=True)
    author = models.CharField(max_length=255, blank=True, help_text='Main author')

    license_text = models.CharField(max_length=255, blank=True)
    license_uri = models.CharField(max_length=255, blank=True)

    nr_blogmarks_sidebar = models.IntegerField(default=20,\
            help_text='Number of blogmarks to list in the sidebar')

    # Social media, galleries etc
    profile_twitter = models.CharField(max_length=255, blank=True)
    profile_googleplus = models.CharField(max_length=255, blank=True)
    profile_linkedin = models.CharField(max_length=255, blank=True)
    profile_flickr = models.CharField(max_length=255, blank=True)
    profile_picasa = models.CharField(max_length=255, blank=True)

    # Statistics-related
    google_analytics_key = models.CharField(max_length=255, blank=True, null=True)
    piwik_analytics_uri = models.CharField(max_length=1024, blank=True, null=True, \
            help_text='Server hostname including http/https, e.g., https://example.com/')
    piwik_analytics_key = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return '{0} {1}'.format(self.site.name, self.template)


class ContentGroup(BaseModel):
    """
    Group of content items; can be used as 'category' for example.
    """
    title = models.CharField(max_length=255)
    site = models.OneToOneField(Site)
    #filter = models.One
    parent = models.ManyToManyField('self', related_name='parent', blank=True)

    def __unicode__(self):
        return '{0} {1}'.format(self.site, self.title)


class Tag(BaseModel):
    """
    Reusable tags to be used to classify articles and such. Can be used to find related items.
    """
    tag = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='tag')

    def __unicode__(self):
        return '{0} [{1}]'.format(self.tag, self.slug)


class Comment(BaseModel):
    """
    Comment on a content item
    """

    # A comment can reference any kind of model, but will be used for models that inherit
    # from BaseContentItem
    # See https://docs.djangoproject.com/en/dev/ref/contrib/contenttypes/#generic-relations
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # Comment is by a logged in user:
    siteuser = models.ForeignKey(SiteUser, blank=True, null=True)
    # Alternatively, a (semi)anonymous visitor:
    name = models.CharField(max_length=255, blank=True, null=True)
    email_address = models.CharField(max_length=255, blank=True, null=True)

    # Source of the comment; the site itself, Facebook, Twitter, other
    COMMENT_SOURCES = (
        (1, _("This site")),
        (2, _("Facebook")),
        (3, _("Twitter")),
        (4, _("Tumblr")),
        (99, _("Other"))
    )
    source = models.IntegerField(choices=COMMENT_SOURCES, default=1)
    original_uri = models.URLField(verbose_name='URI of original comment, if applicable', null=True)

    # IP-address for reference in case of abuse and such
    ip_address = models.GenericIPAddressField()

    # The comment text itself
    comment = models.TextField()

    def __unicode__(self):
        return '{0} {1} {2}'.format(self.content_object, self.ip_address, self.siteuser)


class BaseContentItem(BaseModel):
    """
    Base model containing the shared properties for Article, Link etc.
    """

    """
    ARTICLE = 0
    LINK = 1
    SNIPPET = 2
    IMAGE = 3
    BINARY = 4
    CHOICES = (
            (ARTICLE, 'Article'),
            (LINK, 'Link'),
            (SNIPPET, 'Snippet'),
            (IMAGE, 'Image'),
            (BINARY, 'Attachment'),
    )

    contenttype = models.IntegerField(choices=CHOICES, default=ARTICLE)
    """
    #site = models.ForeignKey(Site, related_name='%(app_label)s_%(class)s_site')
    sites = models.ManyToManyField(Site)
    author = models.ForeignKey(SiteUser, related_name='%(app_label)s_%(class)s_author')
    title = models.CharField(max_length=255, blank=True)
    slug = AutoSlugField(populate_from='title', unique_with='title')
    # When creating a shorturl, use this ID (can be filled with hashids, for example):
    short_id = models.CharField(max_length=20, blank=True, unique=True)
    public = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    published_date = models.DateTimeField(blank=True, null=True)
    publish_from = models.DateTimeField(default=timezone.now, blank=True, null=True)
    publish_to = models.DateTimeField(blank=True, null=True)

    modified_times = models.PositiveIntegerField(default=0)
    #last_modified = models.DateTimeField(blank=True, null=True)

    # Optional location of where the author wrote this article
    location = models.CharField(max_length=255, blank=True)

    tags = models.ManyToManyField(Tag, related_name='%(app_label)s_%(class)s_tags', blank=True)

    protected = models.BooleanField(default=False)
    #password = models.

    # Content item like an article: centered around its body text
    body = models.TextField(blank=True)

    comments_enabled = models.BooleanField(default=True)
    comments = GenericRelation(Comment)

    def publish(self):
        """
        Publish this content now
        """
        self.published = True
        self.published_date = timezone.now()
        self.save()

    def generate_short_id(self):
        hashids = Hashids(salt=settings.HASHIDS_SALT)
        return hashids.encode(self.pk)

    def add_comment(self, siteuser, name, email, comment, ip_address):
        """
        Comment
        """
        comment = Comment(content_object=self, siteuser=siteuser, name=name, email_address=email,\
                ip_address=ip_address, comment=comment)
        comment.save()

    @property
    def comment_count(self):
        """
        Get the amount of comments on this content object
        """
        result = BaseContentItem.objects.select_related().annotate(number_comments=Count('comment'))
        return result[0].number_comments

    @property
    def visible(self):
        """
        Determine whether this content should be visible in the site
        """
        pubfrom = True
        pubto = True
        if self.publish_from:
            pubfrom = self.publish_from <= timezone.now()
        if self.publish_to:
            pubto = timezone.now() <= self.publish_to
        return self.published and pubfrom and pubto


    def save(self, *args, **kwargs):
        if not self.pk:
            # New object, do nothing special for the moment
            pass
        else:
            self.modified_times = self.modified_times + 1
            self.last_modified = timezone.now()
        print 'short_id: [' + self.short_id + ']'
        if not self.short_id:
            self.short_id = self.generate_short_id()
        # short_id is generated after saving is done, as at first, there's no pk yet
        super(BaseContentItem, self).save(*args, **kwargs)

    class Meta:
        abstract = True

signals.post_save.connect(update_short_id, sender=BaseContentItem)


class Article(BaseContentItem):
    """
    Content item like an article: centered around its body text.
    Related to :model:`kontent.Site`
    """
    LONGFORM = 0
    SNIPPET = 1
    CHOICES = (\
            (LONGFORM, 'Article'),
            (SNIPPET, 'Snippet'),)
    articletype = models.IntegerField(choices=CHOICES, default=LONGFORM)

    headline = models.TextField(max_length=255, blank=True)

    def previous_item(self, site):
        """
        Determine the item published before this article
        """
        now = timezone.now()
        previous_items = Article.objects.all().filter(sites__id=site.id, published__lte=self.published).\
                filter(Q(publish_from__lte=now)|Q(publish_from=None)).order_by('-published')
        if previous_items:
            return previous_items[0]
        else:
            return None

    def next_item(self, site):
        """
        Determine the item following this article (if any)
        """
        now = timezone.now()
        next_items = Article.objects.all().filter(sites__id=site.id, published__gte=self.published).\
                filter(Q(publish_from__lte=now)|Q(publish_from=None)).order_by('-published')
        if next_items:
            return next_items[0]
        else:
            return None

    def __unicode__(self):
        return 'Article: {0}'.format(self.title)


class Link(BaseContentItem):
    """
    Content item that links to some external source, informally known as a blogmark
    """
    # If linking to external source
    external_link = models.CharField(max_length=3000, blank=True)
    original_url = models.CharField(max_length=3000, blank=True) # For example a shortened uri

    def save(self, *args, **kwargs):
        #if not self.id and (original_url and not external_link):
        if self.original_url and not self.external_link:
            # Try to de-tiny-fy the url
            self.external_link = self.deredirect(self.original_url)
        super(Link, self).save(*args, **kwargs)

    @classmethod
    def deredirect(cls, uri):
        """
        Try to get the original uri from a shortened/redirectified uri
        """
        import urllib2
        request = urllib2.Request(uri)
        opener = urllib2.build_opener()
        remotesource = opener.open(request)
        return remotesource.url

    @property
    def link(self):
        """
        Return the most relevant uri (e.g., the unshortened short-url)
        """
        if self.external_link:
            return self.external_link
        else:
            return self.original_url

    def __unicode__(self):
        return self.external_link


class Image(BaseContentItem):
    """
    Image item (binary file that's an attachment or download).
    """
    image_width = models.IntegerField(default=0)
    image_height = models.IntegerField(default=0)
    image = models.ImageField(width_field='image_width', height_field='image_height', blank=True)

    def __unicode__(self):
        return self.image.name


class Binary(BaseContentItem):
    """
    Item containing some binary file. Used for attachments, downloads and such
    """
    attachment = models.FileField()

    def __unicode__(self):
        return self.attachment


class Page(BaseContentItem):
    """
    Item containing a (static) page, like some information page as about, or product page
    """
    headline = models.TextField(max_length=255, blank=True)

    def __unicode__(self):
        return 'Page: {0}'.format(self.title)
