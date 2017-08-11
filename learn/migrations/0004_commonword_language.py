# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-11 06:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0003_commonword'),
    ]

    operations = [
        migrations.AddField(
            model_name='commonword',
            name='language',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='learn.Language'),
            preserve_default=False,
        ),
    ]