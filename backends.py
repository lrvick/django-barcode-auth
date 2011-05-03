from django.contrib.auth.models import User

class BarcodeAuthBackend(object):
    """
    Authenticates against a username and a hash contained in a barcode generated 
    by django-barcode-auth.utils.gen_passhash()

    """
    
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username=username)
            known_passhash = gen_passhash(username)
            if password == known_passhash:
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
