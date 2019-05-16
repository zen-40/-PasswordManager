from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PasswordObject
from django.forms import PasswordInput

#Simple registration of a new user
class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    #Remove the tips for 'username' and 'password' that do not look good next the form.
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

#Form for creating a new PasswordObject object
class NewObject(forms.ModelForm):
    class Meta:
        model = PasswordObject
        fields = ['site_name', 'site_url', 'account_name', 'password']

        #Let's cover the displayed fields automatically, they are already shown in the template.
        labels = {
            'site_name': '',
            'site_url': '',
            'account_name': '',
            'password': '',
        }
        widgets = {
            # let's say django that the password field it's need protection and added shadow '*' inside form
            'password': forms.PasswordInput(attrs={'placeholder': '*********'})
        }

#The form for removing object
class DeleteObject(forms.ModelForm):
    class Meta:
        model = PasswordObject
        fields = ()