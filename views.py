from django.middleware.csrf import get_token
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import login
from django.contrib.auth.models import User
from utils import verify_passhash

def barlogin(request,mode='default',query='default'):
    if request.REQUEST.get('barcode_data'):
        barcode_data = request.REQUEST['barcode_data']
        username,passhash = barcode_data.split('|')
        if verify_passhash(username,passhash):
            user = User.objects.get(username=username)
            user.backend='django.contrib.auth.backends.ModelBackend' 
            login(request, user)
        else:
            print 'authentication invalid'
    return render_to_response('login.html', {}, 
        context_instance=RequestContext(request))

