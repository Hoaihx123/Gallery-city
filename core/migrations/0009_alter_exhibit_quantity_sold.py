# Generated by Django 4.2.5 on 2023-09-28 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_exhibit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exhibit',
            name='quantity_sold',
            field=models.IntegerField(default=0),
        ),
    ]