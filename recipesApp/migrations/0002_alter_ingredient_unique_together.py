# Generated by Django 4.0.1 on 2022-01-27 13:24

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipesApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ingredient',
            unique_together={('user', 'name'), ('user', 'articleNumber')},
        ),
    ]
