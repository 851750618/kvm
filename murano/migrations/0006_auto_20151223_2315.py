# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('murano', '0005_murano_package_review_stat'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Murano_package_review',
            new_name='Murano_packages_review',
        ),
    ]
