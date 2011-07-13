from backends import BarcodeAuthBackend
from django.conf import settings
from django.contrib import auth
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect, HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import render_to_response
from django.template import RequestContext
#from django.views.decorators.csrf import csrf_exempt
from barauth.forms import UserCreationForm
from barauth.models import UserBarcode
from barauth.utils import print_card

barcode_auth = BarcodeAuthBackend()


# BE AWARE that uncommenting this introduces security risks. Only do this if
# you need to login from something outside of the Django install
#@csrf_exempt
def login(request):
    if 'barcode_data' in request.REQUEST:
        auth.logout(request)
        barcode_data = request.REQUEST['barcode_data']
        try:
            user_id, password = barcode_data.lstrip('#').split('|')
            user = barcode_auth.authenticate(
                    user_id=user_id,
                    password=password
            )
        except ValueError:
            user = None
        ctxt = {'referer': request.META.get('HTTP_REFERER', '')}
	if user:
            if user.is_active:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                auth.login(request, user)
	else:
	    ctxt['error'] = True
    
        return render_to_response('login.html', ctxt, context_instance=RequestContext(request))

    else:
	return HttpResponseRedirect('/')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('login')
    else:
        form = UserCreationForm()
    return render_to_response("register.html", {
        'form': form,
    }, context_instance=RequestContext(request))


def profile(request, userprofile):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('barauth.views.login', current_app='barauth'))
    else:
        user = User.objects.get(username=userprofile)
        if request.user == user:
            prefill = model_to_dict(user)
            form = UserCreationForm(initial=prefill)
            return render_to_response("profile.html", {
                'form': form,
                'user': user,
                'enable_printing': settings.PRINT_CARDS,
                }, context_instance=RequestContext(request))
        else:
            # Users can only see their own profiles
            return HttpResponseRedirect('/')

def reprint(request, username=None):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('barauth.views.login', current_app='barauth'))
    else:
        user = User.objects.get(username=username)
        if request.user == user:
            barcode = UserBarcode.objects.get(user=user).barcode.name
            print_card(user, barcode)
        # Now they should go get their card, so let's log them out for security
        return HttpResponseRedirect(reverse('barauth.views.logout'))
