# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('murano', '0003_auto_20151219_1440'),
    ]

    operations = [
        migrations.CreateModel(
            name='Murano_package_review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('desc', models.CharField(max_length=3000)),
            ],
        ),
        migrations.DeleteModel(
            name='Users',
        ),
    ]
