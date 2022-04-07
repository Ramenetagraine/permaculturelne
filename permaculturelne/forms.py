from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profil, Message, InscriptionBenevole, InscriptionExposant, InscriptionNewsletter
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

no_space_validator = RegexValidator(
      r' ',
      ("Le pseudonyme ne doit pas contenir d'espaces"),
      inverse_match=True,
      code='invalid_tag',
  )


class ProfilCreationForm(UserCreationForm):
    username = forms.CharField(label="Pseudonyme/identifiant*", help_text="Attention, pas d'espace et les majuscules sont importantes...", validators=[no_space_validator,])
    code_postal = forms.CharField(label="Code postal*", )
    email= forms.EmailField(label="Email*",)
    accepter_conditions = forms.BooleanField(required=True, label="J'ai lu et j'accepte les Conditions Générales d'Utilisation du site",  )

    class Meta(UserCreationForm):
        model = Profil
        fields = ['username', 'email', 'password1',  'password2', 'first_name', 'last_name', 'telephone', 'code_postal', 'accepter_conditions']
        exclude = ['slug', ]

    def save(self, commit = True, is_active=False):
        return super(ProfilCreationForm, self).save(commit)
        self.is_active=is_active



class ProfilChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    email = forms.EmailField(label="Email")
    username = forms.CharField(label="Pseudonyme/identifiant", validators=[no_space_validator,])
    description = forms.CharField(label="Description", help_text="Une description de vous-même", required=False)
    code_postal = forms.CharField(label="Code postal*", )
    inscrit_newsletter = forms.BooleanField(required=False, label="J'accepte de recevoir la newsletter")
    is_equipe = forms.BooleanField(required=False, label="Equipe")
    password=None

    class Meta:
        model = Profil
        fields = ['username', 'email', 'telephone', 'first_name', 'last_name', 'code_postal', 'statut_adhesion', 'inscrit_newsletter','is_equipe']


class ProfilChangeForm_admin(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    email = forms.EmailField(label="Email")
    username = forms.CharField(label="Pseudonyme/identifiant", validators=[no_space_validator,])
    description = forms.CharField(label="Description", initial="Une description de vous même (facultatif)", widget=forms.Textarea)
    code_postal = forms.CharField(label="Code postal*", )
    inscrit_newsletter = forms.BooleanField(required=False)
    a_signe = forms.BooleanField(required=False)
    is_equipe = forms.BooleanField(required=False)
    password = None

    class Meta:
        model = Profil
        fields = ['username', 'first_name', 'last_name', 'email', 'code_postal',  'statut_adhesion','inscrit_newsletter','is_equipe']


    def __init__(self, *args, **kwargs):
        super(ProfilChangeForm_admin, self).__init__(*args, **kwargs)


class ContactForm(forms.Form):
    sujet = forms.CharField(max_length=100, label="Sujet",)
    msg = forms.CharField(label="Message", widget=forms.Textarea)
    renvoi = forms.BooleanField(label="recevoir une copie",
                                     help_text="Cochez si vous souhaitez obtenir une copie du mail envoyé.", required=False
                                 )

class ContactAnonymeForm(forms.Form):
    nom = forms.CharField(max_length=100, label="Nom Prénom",)
    email = forms.EmailField(required=True)
    sujet = forms.CharField(max_length=100, label="Sujet",)
    msg = forms.CharField(label="Message", widget=forms.Textarea)
    renvoi = forms.BooleanField(label="recevoir une copie",
                                     help_text="Cochez si vous souhaitez obtenir une copie du mail envoyé.", required=False
                                 )

class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        exclude = ['auteur', 'date_creation', 'valide']

        widgets = {
                #'message': forms.Textarea(attrs={'rows': 2}),
                'message': SummernoteWidget(),
            }

    def __init__(self, request, message=None, *args, **kwargs):
        super(MessageForm, self).__init__(request, *args, **kwargs)
        if message:
           self.fields['message'].initial = message


class MessageChangeForm(forms.ModelForm):

    class Meta:
        model = Message
        exclude = ['auteur',  'valide']


        widgets = {'message': SummernoteWidget(),     }

class InscriptionBenevoleForm(forms.ModelForm):
    class Meta:
        model = InscriptionBenevole
        fields = ['domaine_benevole', 'jour_mer', 'jour_jeu', 'jour_ven', 'jour_sam', 'description']
        widgets = {'description': SummernoteWidget(),
                   }

    def __init__(self, request, message=None, *args, **kwargs):
        super(InscriptionBenevoleForm, self).__init__(request, *args, **kwargs)
        if message:
           self.fields['description'].initial = message


class InscriptionExposantForm(forms.ModelForm):
    nom_structure = forms.CharField(label="Nom de la structure, association, autre")
    #procedure_lue = forms.BooleanField(label="J'ai lu et compris la procédure d'inscription (en haut de la page)", required=True)

    class Meta:
        model = InscriptionExposant
        fields = ['nom_structure', 'description', 'nombre_tables', 'telephone', ]
        widgets = {
            'description': SummernoteWidget(),
            #'lot_tombola': SummernoteWidget(),
        }

    def __init__(self, request, message=None, *args, **kwargs):
        super(InscriptionExposantForm, self).__init__(request, *args, **kwargs)
        if message:
           self.fields['description'].initial = message



class InscriptionNewsletterForm(forms.ModelForm):

    class Meta:
        model = InscriptionNewsletter
        fields = ['email']

