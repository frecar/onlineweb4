# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_onlineuser_online_mail'),
    ]

    operations = [
        migrations.AddField(
            model_name='onlineuser',
            name='jobmail',
            field=models.BooleanField(default=False, verbose_name='vil ha oppdragsmail'),
            preserve_default=True,
        ),
    ]
