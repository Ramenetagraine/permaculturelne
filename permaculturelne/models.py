# -*- coding: utf-8 -*-
from django.db import models
from django.utils.timezone import now
from django.urls import reverse, reverse_lazy
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
import decimal, math
import os
import requests
from django.template.defaultfilters import slugify

DEGTORAD=3.141592654/180

LATITUDE_DEFAUT = '42.6976'
LONGITUDE_DEFAUT = '2.8954'

class Choix():
    type_message = ('0','Commentaire'), ("1","Coquille"), ('2','Réflexion')
    type_article = ('0','intro'), ("1","constat"), ('2','preconisations'), ('3','charte'), ('4','liens'), ('5','accueil')
    type_benevole = ('0','Accueil'), ("1","Bar"), ('2','Internet'), ('3','Logistique'), ('4','Concert'), ('5', 'Sécurité'), ('6',"N'importe...")
    type_exposant = ('0','Association'), ("1","Particulier"), ('2','Institution'), ('3','Commerçant'), ('4','Nourriture sur place'), ('5','Conférence'), ('6', 'Atelier'), ('7', "autre")
    type_domaine_exposant = ('0','Agriculture'), ("1","Alimentaire"), ('2','Artisanat'), ('3','Bien être'), ('4','Habitat'), ('5','Informations'), ('6', 'Jeux'), ('7', "autre")



class Profil(AbstractUser):
    description = models.TextField(null=True, blank=True)
    code_postal = models.CharField(max_length=5, blank=True, null=True, default="66000")
    commune = models.CharField(max_length=50, blank=True, null=True, default="Perpignan")
    date_registration = models.DateTimeField(verbose_name="Date de création", editable=False)
    inscrit_newsletter = models.BooleanField(verbose_name="J'accepte de recevoir des emails", default=False)
    accepter_conditions = models.BooleanField(verbose_name="J'ai lu et j'accepte les conditions d'utilisation du site", default=False, null=False)

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.username

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.date_registration = now()
        return super(Profil, self).save(*args, **kwargs)

    def get_nom_class(self):
        return "Profil"

    def get_absolute_url(self):
        return reverse('profil', kwargs={'user_id':self.id})

    @property
    def inscrit_newsletter_str(self):
       return "oui" if self.inscrit_newsletter else "non"

class Message(models.Model):
    message = models.TextField(null=False, blank=False)
    auteur = models.ForeignKey(Profil, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    valide = models.BooleanField(verbose_name="validé", default=False)

    def __unicode__(self):
        return self.__str()

    def __str__(self):
        return "(" + str(self.id) + ") " + str(self.auteur) + " " + str(self.date_creation)


class InscriptionBenevole(models.Model):
    user = models.ForeignKey(Profil, on_delete=models.CASCADE)
    domaine_benevole = models.CharField(max_length=10,
        choices=(Choix.type_benevole),
        default='0', verbose_name="Domaine préférentiel du bénévolat")
    jours_festival =models.CharField(max_length=10,
        choices=((0, 'Samedi'), (1, "Dimanche"), (2, "Samedi et dimanche")),
        default='0', verbose_name="Quel(s) jour(s) du festival seriez-vous disponible")
    heures_festival =models.CharField(max_length=10,
        choices=((0, "2h dans la journée"), (3, "Le matin"), (4, "L'après midi"), (5, "Toute la journée")),
        default='0', verbose_name="Combien d'heures")
    dispo_avantfestival = models.TextField(null=False, blank=True, verbose_name="Quelle est votre disponibilité pour venir aider à la mise en place du festival (les jours précédant le festival) ?")
    description = models.TextField(null=False, blank=True, verbose_name="Vous pouvez expliciter ici ce que vous préférez faire, vos disponibilités, etc")
    date_inscription = models.DateTimeField(verbose_name="Date d'inscription", editable=False, auto_now_add=True)

    def __unicode__(self):
        return self.__str()

    def __str__(self):
        return "(" + str(self.id) + ") " + str(self.user) + " " + str(self.date_inscription) + " " + str(self.domaine_benevole) + " " + str(self.description)

    @property
    def get_absolute_url(self):
        return reverse('profil', kwargs={'user_id':self.user.id})
    
class InscriptionExposant(models.Model):
    user = models.ForeignKey(Profil, on_delete=models.CASCADE)
    nom_structure = models.TextField(null=False, blank=True, verbose_name="Nom de la structure, association, autre")

    phone_regex = RegexValidator(regex=r'^\d{9,10}$', message="Le numéro de téléphone doit contenir 10 chiffres")
    telephone = models.CharField(verbose_name="Numéro de téléphone de la personne joignable pendant le festival",validators=[phone_regex,], max_length=10, blank=True)  # validators should be a list

    plaque_regex = RegexValidator(regex=r'^[A-Za-z]{2}[0-9]{3}[A-Za-z]{2}$', message="Le numéro de la plaque minéralogique doit etre au format AA123BB")
    plaque = models.CharField(verbose_name="Numéro de la plaque minéralogique du véhicule utilisé pour le transport du matériel",validators=[plaque_regex,], max_length=10, blank=True)  # validators should be a list

    type_exposant = models.CharField(max_length=10,
        choices=(Choix.type_exposant),
        default='0', verbose_name="Type de la structure")
    domaine_exposant = models.CharField(max_length=10,
        choices=(Choix.type_domaine_exposant),
        default='0', verbose_name="Domaine principal")
    description = models.TextField(null=False, blank=True, verbose_name="Vous pouvez préciser le stand que vous voulez tenir")
    nombre_tables =models.CharField(max_length=10,
        choices=((0, 'pas de table'), (1, "1 table"), (2, "2 tables")),
        default='0', verbose_name="Combien de tables voulez vous réserver ?")
    is_tombola = models.BooleanField(verbose_name="Je souhaite offrir un lot pour la tombola", default=False)
    lot_tombola = models.TextField(null=True, blank=True, verbose_name="Quel lot proposez vous pour la tombola?")

    date_inscription = models.DateTimeField(verbose_name="Date d'inscrition", editable=False, auto_now_add=True)

    def __unicode__(self):
        return self.__str()

    def __str__(self):
        return "(" + str(self.id) + ") " + str(self.user) + " " + str(self.date_inscription) + " " + str(self.domaine_exposant) + " " + str(self.description)


    @property
    def get_absolute_url(self):
        return reverse('profil', kwargs={'user_id':self.user.id})

class InscriptionNewsletter(models.Model):
    email = models.EmailField()
    date_inscription = models.DateTimeField(verbose_name="Date d'inscription", editable=False, auto_now_add=True)

    def __unicode__(self):
        return self.__str()

    def __str__(self):
        return str(self.email)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.date_inscription = now()
        return super(InscriptionNewsletter, self).save(*args, **kwargs)
