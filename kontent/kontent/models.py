from django.db import models
from django.db.models import Q
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericRelation
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from datetime import datetime
import markdown
from django.utils.safestring import mark_safe


class BaseModel(models.Model):
    """
    Base model with common properties.
    """
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
        ordering = ('-date_created', )


class SiteUser(BaseModel):
    """
    User object, like a site admin, editor or authenticated visitor.
    """
    user = models.OneToOneField(User, related_name='authuser')
    website = models.CharField(max_length=255, blank=True, help_text='Optional, website/homepage of this user')

    def is_member(user, groupname):
        """
        Check if user `user` is in group `groupname`
        """
        return user.groups.filter(name=groupname).exists()

    def __unicode__(self):
        return '{0} [{1}]'.format(self.user.first_name, self.user)


class SiteConfig(BaseModel):
    """
    Site-specific configuration.
    """
    site = models.ForeignKey(Site)

    # Custom theme, directory
    template = models.CharField(max_length=255, blank=True)

    # Statistics-related
    google_analytics_key = models.CharField(max_length=255, blank=True, null=True)
    piwik_analytics_uri = models.CharField(max_length=1024, blank=True, null=True, help_text='Server hostname including http/https, e.g., https://example.com/')
    piwik_analytics_key = models.CharField(max_length=255, blank=True, null=True)


class ContentGroup(BaseModel):
    """
    Group of content items; can be used as 'category' for example.
    """
    title = models.CharField(max_length=255)
    site = models.OneToOneField(Site)
    #filter = models.One
    parent = models.ManyToManyField('self', related_name='parent', blank=True)


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

    # IP-address for reference in case of abuse and such
    ip = models.IPAddressField()

    # The comment text itself
    comment = models.TextField()


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
    public = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    published_date = models.DateTimeField(blank=True, null=True)
    publish_from = models.DateTimeField(blank=True, null=True)
    publish_to = models.DateTimeField(blank=True, null=True)

    modified_times = models.PositiveIntegerField(default=0)
    last_modified = models.DateTimeField(blank=True, null=True)

    tags = models.ManyToManyField(Tag, related_name='%(app_label)s_%(class)s_tags', blank=True)

    protected = models.BooleanField(default=False)
    #password = models.

    # Content item like an article: centered around its body text
    body = models.TextField(blank=True)

    comments_enabled = models.BooleanField(default=True)
    comments = GenericRelation(Comment)

    def publish(self):
        self.published = True
        self.published_date = timezone.now()
        self.save()

    def add_comment(self, siteuser, name, email, comment, ip):
        """
        Comment
        """
        c = Comment(content_object=self, siteuser=siteuser, name=name, email_address=email, ip=ip)
        c.save()

    @property
    def visible(self):
        pubfrom = True
        pubto = True
        if self.publish_from:
            pubfrom = self.published_from <= datetime.now()
        if self.publish_to:
            pubto = datetime.now() <= self.publish_to
        return self.published and pubfrom and pubto

    @property
    def body_html(self):
        return mark_safe(markdown.markdown(self.body))


    def save(self, *args, **kwargs):
        if not self.pk:
            # New object, do nothing special for the moment
            pass
        else:
            self.modified_times = self.modified_times + 1
            self.last_modified = datetime.now()
        super(BaseContentItem, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Article(BaseContentItem):
    """
    Content item like an article: centered around its body text.
    Related to :model:`kontent.Site`
    """
    LONGFORM = 0
    SNIPPET = 1
    CHOICES = (
            (LONGFORM, 'Article'),
            (SNIPPET, 'Snippet'),
    )
    articletype = models.IntegerField(choices=CHOICES, default=LONGFORM)

    headline = models.TextField(max_length=255, blank=True)


    def previous_item(self, site):
        #previous = Article.objects.all().filter(sites__id=site.id, visible=True, published_le=article.published).order_by('-published')
        now = datetime.now()
        previous_items = Article.objects.all().filter(sites__id=site.id, published__lte=self.published).filter(Q(publish_from__lte=now)|Q(publish_from=None)).order_by('-published')
        if previous_items:
            return previous_items[0]
        else:
            return None

    def next_item(self, site):
        now = datetime.now()
        next_items = Article.objects.all().filter(sites__id=site.id, published__gte=self.published).filter(Q(publish_from__lte=now)|Q(publish_from=None)).order_by('-published')

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

        super(ContentItem, self).save(*args, **kwargs)

    def deredirect(self, uri):
        """
        Try to get the original uri from a shortened/redirectified uri
        """
        import urllib2, httplib
        request = urllib2.Request(uri)
        opener = urllib2.build_opener()
        f = opener.open(request)
        return f.url


class Image(BaseContentItem):
    """
    Image item (binary file that's an attachment or download).
    """
    image_width = models.IntegerField(default=0)
    image_height = models.IntegerField(default=0)
    image = models.ImageField(width_field=image_width, height_field=image_height, blank=True)


class Binary(BaseContentItem):
    """
    Item containing some binary file. Used for attachments, downloads and such
    """
    attachment = models.FileField()
