# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-12 11:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Definition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='definition',
            name='term',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='definitions.Term'),
        ),
    ]