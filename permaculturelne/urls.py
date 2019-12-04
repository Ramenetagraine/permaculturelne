"""festival URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.urls import path
from permaculturelne import views
from django.views.generic import TemplateView
#from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

# On import les vues de Django, avec un nom spécifique
from django.contrib.auth.decorators import login_required

# admin.autodiscover()
from django.contrib import admin


admin.sites.site_header ="Admin "
admin.sites.site_title ="Admin Permacat"


urlpatterns = [
    path('gestion/', admin.site.urls),
    url(r'^summernote/', include('django_summernote.urls')),
    url(r'^captcha/', include('captcha.urls')),
    url('^', include('django.contrib.auth.urls')),
    url(r'^$', views.bienvenue, name='bienvenue'),
    url(r'^faq/$', views.faq, name='faq'),
    url(r'^contact/$', views.contact, name='contact', ),
    url(r'^cgu/$', views.cgu, name='cgu', ),
    url(r'^liens/$', views.liens, name='liens', ),

    url(r'^accounts/profil/(?P<user_id>[0-9]+)/$', login_required(views.profil), name='profil', ),
    url(r'^accounts/profil/(?P<user_username>[-\w.]+)/$', login_required(views.profil_nom), name='profil_nom', ),
    url(r'^accounts/profile/$', login_required(views.profil_courant), name='profil_courant', ),
    url(r'^accounts/profil_modifier/$', login_required(views.profil_modifier.as_view()), name='profil_modifier',),
    url(r'^accounts/profil_supprimer/$', login_required(views.profil_supprimer.as_view()), name='profil_supprimer',),

    url(r'^benevoles/$', views.benevoles, name='benevoles', ),
    url(r'^exposants/$', views.exposants, name='exposants', ),
    url(r'^benevoles/inscription_benevole/$', views.inscription_benevole, name='inscription_benevole', ),
    url(r'^exposants/inscription_exposant/$', views.inscription_exposant, name='inscription_exposant', ),
    url(r'^contact/$', views.contact, name='contact', ),
    url(r'^organisation/$', views.organisation, name='organisation', ),
    url(r'^forum/$', views.forum, name='forum', ),
    url(r'^inscription_newsletter/$', views.inscription_newsletter, name='inscription_newsletter', ),
    url(r'^voir_inscrits/$', views.voir_inscrits, name='voir_inscrits', ),


    url(r'^merci/$', views.merci, name='merci'),
    url(r'^register/$', views.register, name='senregistrer', ),
    url(r'^password/change/$', views.change_password, name='change_password'),
    path('auth/', include('django.contrib.auth.urls')),
    url(r'^contact_admins/$', views.contact_admins, name='contact_admins',),

]
urlpatterns += [
    url(r'^robots\.txt$', TemplateView.as_view(template_name="permaculturelne/robots.txt", content_type='text/plain')),
]

from django.conf import settings
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'permaculturelne.views.handler404'
handler500 = 'permaculturelne.views.handler500'
handler400 = 'permaculturelne.views.handler400'
handler403 = 'permaculturelne.views.handler403'

if settings.LOCALL:
    import debug_toolbar
    urlpatterns = [url(r'^__debug__/', include(debug_toolbar.urls)),] + urlpatterns
    #urlpatterns += url('',(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}))