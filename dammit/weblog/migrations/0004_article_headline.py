# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weblog', '0003_auto_20141213_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='headline',
            field=models.TextField(default='', max_length=255, blank=True),
            preserve_default=False,
        ),
    ]
