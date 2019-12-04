from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profil, Message, InscriptionBenevole, InscriptionExposant, InscriptionNewsletter
from captcha.fields import CaptchaField
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

no_space_validator = RegexValidator(
      r' ',
      ("Le pseudonyme ne doit pas contenir d'espaces"),
      inverse_match=True,
      code='invalid_tag',
  )


class ProfilCreationForm(UserCreationForm):
    username = forms.CharField(label="Pseudonyme*", help_text="Attention les majuscules sont importantes...", validators=[no_space_validator,])
    description = forms.CharField(label=None, help_text="Une description de vous même", required=False, widget=forms.Textarea)
    code_postal = forms.CharField(label="Code postal*", )
    commune = forms.CharField(label="Commune*", )
    email= forms.EmailField(label="Email*",)
    accepter_conditions = forms.BooleanField(required=True, label="J'ai lu et j'accepte les Conditions Générales d'Utilisation du site",  )
    captcha = CaptchaField()

    class Meta(UserCreationForm):
        model = Profil
        fields = ['username', 'email', 'password1',  'password2', 'first_name', 'last_name',  'description', 'code_postal', 'commune', 'inscrit_newsletter', 'accepter_conditions']
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
    username = forms.CharField(label="Pseudonyme", validators=[no_space_validator,])
    description = forms.CharField(label="Description", help_text="Une description de vous-même", required=False)
    code_postal = forms.CharField(label="Code postal*", )
    commune = forms.CharField(label="Commune*", )
    inscrit_newsletter = forms.BooleanField(required=False, label="J'accepte de recevoir la newsletter")
    password=None

    class Meta:
        model = Profil
        fields = ['username', 'email', 'first_name', 'last_name',  'description', 'code_postal', 'commune', 'inscrit_newsletter']


class ProfilChangeForm_admin(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    email = forms.EmailField(label="Email")
    username = forms.CharField(label="Pseudonyme", validators=[no_space_validator,])
    description = forms.CharField(label="Description", initial="Une description de vous même (facultatif)", widget=forms.Textarea)
    code_postal = forms.CharField(label="Code postal*", )
    commune = forms.CharField(label="Commune*", )
    inscrit_newsletter = forms.BooleanField(required=False)
    accepter_annuaire = forms.BooleanField(required=False)
    a_signe = forms.BooleanField(required=False)
    password = None

    class Meta:
        model = Profil
        fields = ['username', 'first_name', 'last_name', 'email', 'description', 'code_postal', 'commune', 'inscrit_newsletter']


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
    message = forms.CharField(label="Laisser un commentaire...",)

    class Meta:
        model = Message
        exclude = ['auteur', 'date_creation', 'valide']

        widgets = {
                'message': forms.Textarea(attrs={'rows': 2}),
            }

    def __init__(self, request, message=None, *args, **kwargs):
        super(MessageForm, self).__init__(request, *args, **kwargs)
        if message:
           self.fields['message'].initial = message


class InscriptionBenevoleForm(forms.ModelForm):

    class Meta:
        model = InscriptionBenevole
        fields = ['domaine_benevole', 'description']
        widgets = {'description': SummernoteWidget()}

    def __init__(self, request, message=None, *args, **kwargs):
        super(InscriptionBenevoleForm, self).__init__(request, *args, **kwargs)
        if message:
           self.fields['description'].initial = message



class InscriptionExposantForm(forms.ModelForm):

    class Meta:
        model = InscriptionExposant
        fields = ['domaine_exposant', 'description']
        widgets = {'description': SummernoteWidget()}

    def __init__(self, request, message=None, *args, **kwargs):
        super(InscriptionExposantForm, self).__init__(request, *args, **kwargs)
        if message:
           self.fields['description'].initial = message



class InscriptionNewsletterForm(forms.ModelForm):

    class Meta:
        model = InscriptionNewsletter
        fields = ['email']

