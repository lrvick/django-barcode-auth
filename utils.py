import hashlib
from django.contrib.auth.models import User
from django.conf import settings

def gen_passhash(username):
    user = User.objects.get(username=username)
    token_handle = hashlib.sha224()
    token_handle.update(username) 
    token_handle.update(user.password)
    token_handle.update(settings.SECRET_KEY)
    hex_hash = token_handle.hexdigest() 
    return hex_hash
