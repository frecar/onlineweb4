# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_jobmail_set_true'),
    ]

    operations = [
        migrations.AddField(
            model_name='onlineuser',
            name='bio',
            field=models.TextField(null=True, verbose_name='bio', blank=True),
            preserve_default=True,
        ),
    ]
