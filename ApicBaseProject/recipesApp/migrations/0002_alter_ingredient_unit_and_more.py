# Generated by Django 4.0.1 on 2022-01-25 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipesApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='unit',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='r_amount',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
    ]
