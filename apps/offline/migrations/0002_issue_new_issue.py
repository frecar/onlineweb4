# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offline', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='new_issue',
            field=models.FileField(upload_to=b'images/offline', max_length=500, verbose_name='pdf', blank=True),
            preserve_default=True,
        ),
    ]
