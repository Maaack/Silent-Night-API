# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-14 22:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game_api', '0005_defaultgamesettings_defaultspacesettings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='defaultspacesettings',
            name='gamesettings_ptr',
        ),
        migrations.DeleteModel(
            name='DefaultSpaceSettings',
        ),
    ]
