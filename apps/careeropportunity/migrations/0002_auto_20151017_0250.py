# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('careeropportunity', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='careeropportunity',
            options={'verbose_name': 'karrieremulighet', 'verbose_name_plural': 'karrieremuligheter', 'permissions': (('view_careeropportunity', 'View CareerOpportunity'), ('change_careeropportunity', 'Change CareerOpportunity'))},
        ),
    ]
