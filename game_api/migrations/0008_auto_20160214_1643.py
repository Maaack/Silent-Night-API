# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-15 00:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game_api', '0007_defaultspacesettings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='space',
            name='initial_snapshot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='game_api.Snapshot'),
        ),
        migrations.AlterField(
            model_name='space',
            name='seed',
            field=models.CharField(max_length=50, null=True, verbose_name='Random Seed'),
        ),
    ]
