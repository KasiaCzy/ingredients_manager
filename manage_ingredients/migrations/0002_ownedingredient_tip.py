# Generated by Django 3.1.3 on 2020-11-10 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_ingredients', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ownedingredient',
            name='tip',
            field=models.CharField(default='...', max_length=16),
        ),
    ]
