# Generated by Django 2.2.2 on 2019-08-19 15:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="testmodel",
            name="active",
            field=models.BooleanField(default=True),
        ),
    ]
