# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('murano', '0008_package_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='package_review',
            name='path',
            field=models.CharField(default='pending', max_length=100),
            preserve_default=False,
        ),
    ]
