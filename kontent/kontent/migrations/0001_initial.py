# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('headline', models.TextField(max_length=255, blank=True)),
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
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContentGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('title', models.CharField(max_length=255)),
                ('parent', models.ManyToManyField(related_name='parent_rel_+', to='kontent.ContentGroup', blank=True)),
                ('site', models.OneToOneField(to='sites.Site')),
            ],
            options={
                'ordering': ('-date_created',),
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
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SiteConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('template', models.CharField(max_length=255, blank=True)),
                ('site', models.ForeignKey(to='sites.Site')),
            ],
            options={
                'ordering': ('-date_created',),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SiteUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('website', models.CharField(max_length=255)),
                ('user', models.OneToOneField(related_name='authuser', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-date_created',),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('tag', models.CharField(max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
            ],
            options={
                'ordering': ('-date_created',),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='link',
            name='author',
            field=models.ForeignKey(related_name='kontent_link_author', to='kontent.SiteUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='link',
            name='sites',
            field=models.ManyToManyField(to='sites.Site'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='link',
            name='tags',
            field=models.ManyToManyField(related_name='kontent_link_tags', to='kontent.Tag', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='image',
            name='author',
            field=models.ForeignKey(related_name='kontent_image_author', to='kontent.SiteUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='image',
            name='sites',
            field=models.ManyToManyField(to='sites.Site'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='image',
            name='tags',
            field=models.ManyToManyField(related_name='kontent_image_tags', to='kontent.Tag', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='binary',
            name='author',
            field=models.ForeignKey(related_name='kontent_binary_author', to='kontent.SiteUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='binary',
            name='sites',
            field=models.ManyToManyField(to='sites.Site'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='binary',
            name='tags',
            field=models.ManyToManyField(related_name='kontent_binary_tags', to='kontent.Tag', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(related_name='kontent_article_author', to='kontent.SiteUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='sites',
            field=models.ManyToManyField(to='sites.Site'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(related_name='kontent_article_tags', to='kontent.Tag', blank=True),
            preserve_default=True,
        ),
    ]
