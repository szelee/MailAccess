from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response
from GoogleMailAccess import settings
from allauth.socialaccount.models import SocialToken
from django.contrib import auth
from app.models import CredentialsModel
from GoogleMailAccess import gmailAPI 

import httplib2
import argparse
import json

from apiclient.discovery import build
from oauth2client.client import Flow

import os
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from oauth2client import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.django_orm import Storage

# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>
CLIENT_SECRETS = settings.GMAIL_CLIENT_SECRETS

FLOW = flow_from_clientsecrets(
    CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/gmail.readonly',
    redirect_uri='http://localhost:8000/oauth2callback')

def login(request):
    return render_to_response('account/login.html')

@login_required
def auth_gmail(request):
    print ("Authenticaion Gmail request")
    storage = Storage(CredentialsModel, 'id', request.user.id, 'credential')
    credential = storage.get()
    print ("credential: %s" % credential)
    if credential is None or credential.invalid == True:
        print ("call authentication")
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                   request.user)
        authorize_url = FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)
    else:
        print ("in the else statement whenre authenticated")
        http = httplib2.Http()
        http = credential.authorize(http)
        service = build("gmail", "v1", http=http)

        threads = service.users().threads().list(userId='me').execute()
        messages = service.users().messages().list(userId='me', q='reservation confirmation').execute()
        #activities = service.activities()
        #activitylist = activities.list(collection='public', 
        #                               userId='me').execute()
        #logging.info(threads)

        return render_to_response('app/welcome.html', {
            'threads': messages['messages'],
            })

@login_required
def auth_return(request):
    print ("in authentication return")
    if not xsrfutil.validate_token(settings.SECRET_KEY, request.REQUEST['state'],
                                   request.user):
        return  HttpResponseBadRequest()
    print ("before exchange the credential")
    credential = FLOW.step2_exchange(request.REQUEST)
    print ("After exchange credential")
    storage = Storage(CredentialsModel, 'id', request.user, 'credential')
    storage.put(credential)
    return HttpResponseRedirect("/")

def get_email(request):
    storage = Storage(CredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    service = gmailAPI.build_service(credential)
    messages = gmailAPI.ListMessages(service, 'me', 'reservation confirmation')
    with open('gmail-data.json', 'w') as outfile:
        json.dump(messages, outfile)
    outfile.close()

    for message in messages:
        email = gmailAPI.GetMessage(service, 'me', message['id'])
        with open('email' + message['id'] + '.txt', 'w') as outfile:
            json.dump(email, outfile)
        outfile.close()

    return HttpResponseRedirect("/")