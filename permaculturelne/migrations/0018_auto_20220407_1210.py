# Generated by Django 2.2.27 on 2022-04-07 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permaculturelne', '0017_auto_20220407_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profil',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='Asresse email'),
        ),
        migrations.AlterField(
            model_name='profil',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='Prénom'),
        ),
        migrations.AlterField(
            model_name='profil',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='Nom'),
        ),
    ]