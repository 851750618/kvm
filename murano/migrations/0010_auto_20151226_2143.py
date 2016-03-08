# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('murano', '0009_package_review_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='package_review',
            name='author',
            field=models.CharField(default='lin', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='package_review',
            name='create_time',
            field=models.DateTimeField(default='2015-12-26 21:43', auto_now_add=True),
            preserve_default=False,
        ),
    ]
