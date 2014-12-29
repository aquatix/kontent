from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from autoslug import AutoSlugField
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
    website = models.CharField(max_length=255)

    def __unicode__(self):
        return '{0} [{1}]'.format(self.user.first_name, self.user)


class SiteConfig(BaseModel):
    """
    Site-specific configuration.
    """
    site = models.ForeignKey(Site)

    # TODO: model?
    template = models.CharField(max_length=255, blank=True)

    # Statistics-related
    google_analytics_key = models.CharField(max_length=255, blank=True, null=True)
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
    publish_from = models.DateTimeField(blank=True, null=True)
    publish_to = models.DateTimeField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='%(app_label)s_%(class)s_tags', blank=True)

    protected = models.BooleanField(default=False)
    #password = models.

    # Content item like an article: centered around its body text
    body = models.TextField(blank=True)

    @property
    def body_html(self):
        return mark_safe(markdown.markdown(self.body))

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


class Link(BaseContentItem):
    """
    Content item that links to some external source, informally known as a blogmark
    """
    # If linking to external source
    external_link = models.CharField(max_length=3000, blank=True)
    original_url = models.CharField(max_length=3000, blank=True) # For example a shorted uri

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
