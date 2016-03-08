# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('murano', '0007_delete_murano_packages_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='Package_review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('desc', models.CharField(max_length=3000)),
                ('status', models.CharField(max_length=30)),
            ],
        ),
    ]
