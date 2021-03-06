# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0005_responsiveimage_image_wide'),
    ]

    operations = [
        migrations.AlterField(
            model_name='responsiveimage',
            name='image_wide',
            field=models.ImageField(upload_to=b'images/responsive/wide', verbose_name='Bredformat'),
            preserve_default=True,
        ),
    ]
