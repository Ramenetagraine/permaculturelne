# Generated by Django 2.2.9 on 2020-01-29 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permaculturelne', '0005_auto_20200129_2004'),
    ]

    operations = [
        migrations.AddField(
            model_name='inscriptionexposant',
            name='jours_festival',
            field=models.CharField(choices=[('0', '----------'), ('1', 'Samedi'), ('2', 'Dimanche'), ('3', 'Samedi et dimanche')], default='0', max_length=10, verbose_name='Quel(s) jour(s) du festival seriez-vous présent ?'),
        ),
    ]
