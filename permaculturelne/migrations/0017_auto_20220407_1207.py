# Generated by Django 2.2.27 on 2022-04-07 10:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('permaculturelne', '0016_auto_20220407_1144'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profil',
            name='commune',
        ),
        migrations.RemoveField(
            model_name='profil',
            name='description',
        ),
    ]
