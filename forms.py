from django.contrib.auth.forms import UserCreationForm
from models import UserBarcode

class BarauthUserCreationForm(UserCreationForm):
    def save
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.barcode = UserBarcode()
        if commit:
            user.save()
        return user

    
