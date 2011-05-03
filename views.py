from django.middleware.csrf import get_token
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from backends import BarcodeAuthBackend

barcode_auth = BarcodeAuthBackend()

def login(request,mode='default',query='default'):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        if request.REQUEST.get('barcode_data'):
            barcode_data = request.REQUEST['barcode_data']
            try: 
                username,password = barcode_data.split('|')
                user = barcode_auth.authenticate(username=username,password=password)
            except ValueError:
                user = None
            if user is not None:
                if user.is_active():
                    user.backend='django.contrib.auth.backends.ModelBackend' 
                    auth.login(request, user)
                    return HttpResponseRedirect('/')
        return render_to_response('login.html', {}, 
            context_instance=RequestContext(request))
