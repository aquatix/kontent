# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weblog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='key',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
