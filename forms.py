from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        #exclude = ('user_permissions', 'groups', 'is_active', 'is_supervisor', 'last_login', 'date_joined')
        fields = ('username', 'first_name', 'last_name', 'email')

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("A user with that username already exists.")

    def clean_password2(self):
        pass1 = self.cleaned_data.get('password1')
        pass2 = self.cleaned_data.get('password2')
        if pass1 or pass2:
            if pass1 != pass2:
                raise forms.ValidationError("The two password fields didn't match")
        return pass2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            send_mail(
                    subject='Thank you for registering at our Mayo kiosk',
                    message='Saving user: %s' % user,
                    from_email=settings.EMAIL_FROM,
                    recipient_list=[user.email],
                    fail_silently=True
                    )
            user.save()
        return user
