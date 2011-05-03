from django.middleware.csrf import get_token
from django.shortcuts import render_to_response
from django.template import RequestContext

def login(request,mode='default',query='default'):
    return render_to_response('login.html', {}, 
        context_instance=RequestContext(request))

