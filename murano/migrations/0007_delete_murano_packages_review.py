# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('murano', '0006_auto_20151223_2315'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Murano_packages_review',
        ),
    ]
