# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('title', models.CharField(max_length=255)),
                ('parent', models.ManyToManyField(related_name='parent_rel_+', to='weblog.ContentGroup', blank=True)),
            ],
            options={
                'ordering': ('-date_created',),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContentItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('contenttype', models.IntegerField(default=0, choices=[(0, b'Article'), (1, b'Link'), (2, b'Snippet'), (3, b'Image'), (4, b'Attachment')])),
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
                ('image_width', models.IntegerField(default=0)),
                ('image_height', models.IntegerField(default=0)),
                ('image', models.ImageField(height_field=models.IntegerField(default=0), width_field=models.IntegerField(default=0), upload_to=b'', blank=True)),
            ],
            options={
                'ordering': ('-date_created',),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContentObject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('protected', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-date_created',),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('title', models.CharField(max_length=255)),
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
            model_name='site',
            name='owner',
            field=models.OneToOneField(related_name='site', to='weblog.SiteUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contentobject',
            name='site',
            field=models.OneToOneField(to='weblog.Site'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contentitem',
            name='author',
            field=models.ForeignKey(related_name='author', to='weblog.SiteUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contentitem',
            name='site',
            field=models.ForeignKey(related_name='site', to='weblog.Site'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contentitem',
            name='tags',
            field=models.ManyToManyField(related_name='tags', to='weblog.Tag', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contentgroup',
            name='site',
            field=models.OneToOneField(to='weblog.Site'),
            preserve_default=True,
        ),
    ]
