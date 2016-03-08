# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('murano', '0004_auto_20151223_2305'),
    ]

    operations = [
        migrations.AddField(
            model_name='murano_package_review',
            name='stat',
            field=models.CharField(default='a', max_length=30),
            preserve_default=False,
        ),
    ]
