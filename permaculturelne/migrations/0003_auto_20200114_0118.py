# Generated by Django 2.2.8 on 2020-01-14 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permaculturelne', '0002_auto_20200114_0113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inscriptionbenevole',
            name='heures_festival',
            field=models.CharField(choices=[('0', '----------'), ('1', '2h dans la journée'), ('2', 'Le matin'), ('3', "L'après midi"), ('4', 'Toute la journée')], default='0', max_length=10, verbose_name="Combien d'heures"),
        ),
        migrations.AlterField(
            model_name='inscriptionbenevole',
            name='jours_festival',
            field=models.CharField(choices=[('0', '----------'), ('1', 'Samedi'), ('2', 'Dimanche'), ('3', 'Samedi et dimanche')], default='0', max_length=10, verbose_name='Quel(s) jour(s) du festival seriez-vous disponible'),
        ),
        migrations.AlterField(
            model_name='inscriptionexposant',
            name='nombre_tables',
            field=models.CharField(choices=[('0', '----------'), ('1', 'pas de table'), ('2', '1 table'), ('3', '2 tables')], default='0', max_length=10, verbose_name='Combien de tables voulez vous réserver ?'),
        ),
    ]
