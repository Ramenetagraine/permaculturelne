# Generated by Django 2.2.27 on 2022-04-07 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permaculturelne', '0018_auto_20220407_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profil',
            name='telephone',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]