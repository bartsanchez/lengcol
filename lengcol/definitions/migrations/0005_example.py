# Generated by Django 2.2.2 on 2019-06-24 16:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('definitions', '0004_term_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Example',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('value', models.TextField()),
                ('definition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='definitions.Definition')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
