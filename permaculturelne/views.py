from django.shortcuts import render, redirect
from django.db.models import CharField
from django.db.models.functions import Lower
from django.views.decorators.debug import sensitive_variables
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.core.mail import mail_admins, send_mail, BadHeaderError
from .forms import ProfilCreationForm, ContactForm, ProfilChangeForm, MessageForm, InscriptionBenevoleForm, InscriptionExposantForm, ContactAnonymeForm, InscriptionNewsletterForm
from .models import Profil, Message, InscriptionNewsletter, InscriptionBenevole, InscriptionExposant
from django.views.generic import ListView, UpdateView, DeleteView
CharField.register_lookup(Lower, "lower")


def handler404(request, template_name="404.html"):  #page not found
    response = render(request, "404.html")
    response.status_code = 404
    return response

def handler500(request, template_name="500.html"):   #erreur du serveur
    response = render(request, "500.html")
    response.status_code = 500
    return response

def handler403(request, template_name="403.html"):   #non autorisé
    response = render(request, "403.html")
    response.status_code = 403
    return response

def handler400(request, template_name="400.html"):   #requete invalide
    response = render(request, "400.html")
    response.status_code = 400
    return response

def bienvenue(request):
    return render(request, 'index.html',)


def presentation_site(request):
    return render(request, 'presentation_site.html')

def merci(request):
    return render(request, 'merci.html')

def faq(request):
    return render(request, 'faq.html')

def cgu(request):
    return render(request, 'cgu.html')


def fairedon(request):
    return render(request, 'fairedon.html', )


@sensitive_variables('user', 'password1', 'password2')
def register(request):
    if request.user.is_authenticated:
        return render(request, "erreur.html", {"msg": "Vous êtes déjà inscrit et connecté !"})

    form_profil = ProfilCreationForm(request.POST or None)
    if form_profil.is_valid():
        profil_courant = form_profil.save(commit=False, is_active=False)
        profil_courant.save()
        return render(request, 'userenattente.html')

    return render(request, 'registration/register.html', { "form_profil": form_profil, })


@login_required
class profil_modifier_user(UpdateView):
    model = Profil
    form_class = ProfilChangeForm
    template_name_suffix = '_modifier'
    fields = ['username', 'first_name', 'last_name', 'email','description', 'inscrit_newsletter']

    def get_object(self):
        return Profil.objects.get(id=self.request.user.id)



class profil_modifier(UpdateView):
    model = Profil
    form_class = ProfilChangeForm
    template_name_suffix = '_modifier'

    def get_object(self):
        return Profil.objects.get(id=self.request.user.id)


class profil_supprimer(DeleteView):
    model = Profil
    success_url = reverse_lazy('bienvenue')

    def get_object(self):
        return Profil.objects.get(id=self.request.user.id)


@sensitive_variables('password')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_changer_form.html', {
        'form': form
    })


def contact(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ContactForm(request.POST or None, )
        else:
            form = ContactAnonymeForm(request.POST or None, )
        if form.is_valid():
            sujet = form.cleaned_data['sujet']

            if request.user.is_authenticated:
                message_txt = request.user.username + " a envoyé le message suivant : "
                message_html = form.cleaned_data['msg']
                email = request.user.email
                nom = request.user.username
            else:
                message_txt = form.cleaned_data['nom'] + " a envoyé le message suivant : "
                message_html = "(nom : " + form.cleaned_data['nom'] + "; email : " + form.cleaned_data['email'] + ")\\n"
                message_html += form.cleaned_data['msg']
                email = form.cleaned_data['email']
                nom = form.cleaned_data['nom']

            try:
                mail_admins(sujet, message_txt, html_message=message_html)
                if form.cleaned_data['renvoi']:
                    send_mail(sujet, message_txt, email, email, fail_silently=False, html_message=message_html)


                return render(request, 'message_envoye.html', {'sujet': sujet, 'msg': message_html,
                                                       'envoyeur': nom + " (" + email + ")",
                                                       "destinataire": "administrateurs "})
            except BadHeaderError:
                return render(request, 'erreur.html', {'msg':'Invalid header found.'})

            return render(request, 'erreur.html', {'msg':"Désolé, une ereur s'est produite"})
    else:
        if request.user.is_authenticated:
            form = ContactForm(request.POST or None, )
        else:
            form = ContactAnonymeForm(request.POST or None, )
    return render(request, 'contact.html', {'form': form})




def contact_admins(request):
    if request.method == 'POST':
        form = ContactForm(request.POST or None, )
        if form.is_valid():
            sujet = form.cleaned_data['sujet']
            message_txt = request.user.username + " a envoyé le message suivant : "
            message_html = form.cleaned_data['msg']
            try:
                mail_admins(sujet, message_txt, html_message=message_html)
                if form.cleaned_data['renvoi']:
                    send_mail(sujet, message_txt, request.user.email, request.user.email, fail_silently=False, html_message=message_html)

                return render(request, 'message_envoye.html', {'sujet': sujet, 'msg': message_html,
                                                       'envoyeur': request.user.username + " (" + request.user.email + ")",
                                                       "destinataire": "administrateurs "})
            except BadHeaderError:
                return render(request, 'erreur.html', {'msg':'Invalid header found.'})

            return render(request, 'erreur.html', {'msg':"Désolé, une ereur s'est produite"})
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form, "isContactProducteur":False})


def liens(request):
    liens = [
        'https://www.facebook.com/ramenetagraine/',
        'https://www.facebook.com/permapat/',
        'https://www.permapat.com/',
        'http://www.perma.cat',
        'https://framacarte.org/m/3427/ ',
        'https://alternatiba.eu/alternatiba66/',
    ]

    return render(request, 'liens.html', {'liens':liens, })


@login_required
def forum(request, ):
    messages = Message.objects.all().order_by("date_creation")
    form = MessageForm(request.POST or None)
    if form.is_valid():
        message = form.save(commit=False)
        message.auteur = request.user
        message.save()
        return redirect(request.path)
    return render(request, 'forum.html', {'form': form, 'messages_echanges': messages})



@login_required
def profil_courant(request, ):
    return render(request, 'registration/profil.html', {'user': request.user})


@login_required
def profil(request, user_id):
    try:
        user = Profil.objects.get(id=user_id)
        return render(request, 'registration/profil.html', {'user': user})
    except User.DoesNotExist:
            return render(request, 'registration/profil_inconnu.html', {'userid': user_id})

@login_required
def profil_nom(request, user_username):
    try:
        user = Profil.objects.get(username=user_username)
        return render(request, 'registration/profil.html', {'user': user, })
    except User.DoesNotExist:
        return render(request, 'registration/profil_inconnu.html', {'userid': user_username})


def benevoles(request):
    return render(request, 'permaculturelne/benevoles.html', )


@login_required
def inscription_benevole(request):
    form = InscriptionBenevoleForm(request.POST or None)
    if form.is_valid():
        inscription = form.save(commit=False)
        inscription.user = request.user
        inscription.save()
        return render(request, 'merci.html', {'msg' :"Votre inscription en tant que bénévole a bien été enregistrée. Vous serez contacté dès que possible. "})

    return render(request, 'permaculturelne/inscription_benevole.html', {'form':form})


def exposants(request):
    return render(request, 'permaculturelne/exposants.html', )


@login_required
def inscription_exposant(request):
    form = InscriptionExposantForm(request.POST or None)
    if form.is_valid():
        inscription = form.save(commit=False)
        inscription.user = request.user
        inscription.save()
        return render(request, 'merci.html', {'msg' :"Votre inscription a bien été enregistrée. Vous serez contacté dès que possible. "})
    return render(request, 'permaculturelne/inscription_exposant.html', {'form':form})

def organisation(request, ):
    return render(request, 'permaculturelne/organisation.html')


def inscription_newsletter(request):
    form = InscriptionNewsletterForm(request.POST or None)
    if form.is_valid():
        inscription = form.save(commit=False)
        inscription.save()
        return render(request, 'merci.html', {'msg' :"Vous êtes inscrits à la newsletter"})
    return render(request, 'inscription_newsletter.html', {'form':form})


def voir_inscrits(request):
    newsletter = InscriptionNewsletter.objects.all()
    news_inscrits = Profil.objects.filter(inscrit_newsletter=True)
    inscription_exposant = InscriptionExposant.objects.all()
    inscription_benevole = InscriptionBenevole.objects.all()


    return render(request, 'permaculturelne/voir_inscrits.html', {'newsletter':newsletter, 'news_inscrits':news_inscrits, 'benevoles':inscription_benevole, 'exposants':inscription_exposant})