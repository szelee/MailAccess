"""
Definition of urls for GoogleMailAccess.
"""

from datetime import datetime
from django.conf.urls import patterns, url
from app.forms import BootstrapAuthenticationForm

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin, auth
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'app.views.home', name='home'),
    url(r'^contact$', 'app.views.contact', name='contact'),
    url(r'^about', 'app.views.about', name='about'),
    #url(r'^contact/login/$', 'GoogleMailAccess.views.login'),
    #url(r'^contact/auth/$', 'GoogleMailAccess.views.auth_gmail'),
    #url(r'^contact/auth_success/$', 'GoogleMailAccess.views.auth_success'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^oauth2callback', 'GoogleMailAccess.views.auth_return'),
    url(r'^google_login/$', 'GoogleMailAccess.views.auth_gmail'),
    url(r'^get_gmail/$', 'GoogleMailAccess.views.get_email'),
    #url(r'^login/$', 'GoogleMailAccess.views.login'),
    url(r'^login/$',
        'django.contrib.auth.views.login',
        {
            'template_name': 'app/login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title':'Log in',
                'year':datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        'django.contrib.auth.views.logout',
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
