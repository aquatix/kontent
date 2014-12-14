# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('weblog', '0002_site_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('title', models.CharField(max_length=255, blank=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
                ('public', models.BooleanField(default=False)),
                ('published', models.BooleanField(default=False)),
                ('publish_from', models.DateTimeField(null=True, blank=True)),
                ('publish_to', models.DateTimeField(null=True, blank=True)),
                ('protected', models.BooleanField(default=False)),
                ('body', models.TextField(blank=True)),
                ('articletype', models.IntegerField(default=0, choices=[(0, b'Article'), (1, b'Snippet')])),
                ('author', models.ForeignKey(related_name='weblog_article_author', to='weblog.SiteUser')),
                ('site', models.ForeignKey(related_name='weblog_article_site', to='weblog.Site')),
                ('tags', models.ManyToManyField(related_name='weblog_article_tags', to='weblog.Tag', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Binary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('title', models.CharField(max_length=255, blank=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
                ('public', models.BooleanField(default=False)),
                ('published', models.BooleanField(default=False)),
                ('publish_from', models.DateTimeField(null=True, blank=True)),
                ('publish_to', models.DateTimeField(null=True, blank=True)),
                ('protected', models.BooleanField(default=False)),
                ('body', models.TextField(blank=True)),
                ('attachment', models.FileField(upload_to=b'')),
                ('author', models.ForeignKey(related_name='weblog_binary_author', to='weblog.SiteUser')),
                ('site', models.ForeignKey(related_name='weblog_binary_site', to='weblog.Site')),
                ('tags', models.ManyToManyField(related_name='weblog_binary_tags', to='weblog.Tag', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('title', models.CharField(max_length=255, blank=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
                ('public', models.BooleanField(default=False)),
                ('published', models.BooleanField(default=False)),
                ('publish_from', models.DateTimeField(null=True, blank=True)),
                ('publish_to', models.DateTimeField(null=True, blank=True)),
                ('protected', models.BooleanField(default=False)),
                ('body', models.TextField(blank=True)),
                ('image_width', models.IntegerField(default=0)),
                ('image_height', models.IntegerField(default=0)),
                ('image', models.ImageField(height_field=models.IntegerField(default=0), width_field=models.IntegerField(default=0), upload_to=b'', blank=True)),
                ('author', models.ForeignKey(related_name='weblog_image_author', to='weblog.SiteUser')),
                ('site', models.ForeignKey(related_name='weblog_image_site', to='weblog.Site')),
                ('tags', models.ManyToManyField(related_name='weblog_image_tags', to='weblog.Tag', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('title', models.CharField(max_length=255, blank=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
                ('public', models.BooleanField(default=False)),
                ('published', models.BooleanField(default=False)),
                ('publish_from', models.DateTimeField(null=True, blank=True)),
                ('publish_to', models.DateTimeField(null=True, blank=True)),
                ('protected', models.BooleanField(default=False)),
                ('body', models.TextField(blank=True)),
                ('external_link', models.CharField(max_length=3000, blank=True)),
                ('original_url', models.CharField(max_length=3000, blank=True)),
                ('author', models.ForeignKey(related_name='weblog_link_author', to='weblog.SiteUser')),
                ('site', models.ForeignKey(related_name='weblog_link_site', to='weblog.Site')),
                ('tags', models.ManyToManyField(related_name='weblog_link_tags', to='weblog.Tag', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='contentitem',
            name='author',
        ),
        migrations.RemoveField(
            model_name='contentitem',
            name='site',
        ),
        migrations.RemoveField(
            model_name='contentitem',
            name='tags',
        ),
        migrations.DeleteModel(
            name='ContentItem',
        ),
        migrations.RemoveField(
            model_name='contentobject',
            name='site',
        ),
        migrations.DeleteModel(
            name='ContentObject',
        ),
    ]
