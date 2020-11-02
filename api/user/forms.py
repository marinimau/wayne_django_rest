#
#   wayne_django_rest copyright © 2020 - all rights reserved
#   Created at: 26/10/2020
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/wayne_django_rest
#   Credits: @marinimau (https://github.com/marinimau)
#

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# ----------------------------------------------------------------------------------------------------------------------
#   Sign-up method for no-staff user
# ----------------------------------------------------------------------------------------------------------------------

class ProfileSignUpForm(UserCreationForm):

    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    name = forms.CharField()
    surname = forms.CharField()
    gender = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'name', 'surname', 'birth_date', 'gender']


# ----------------------------------------------------------------------------------------------------------------------
#   Sign-in method for no-staff user
# ----------------------------------------------------------------------------------------------------------------------

class ProfileSignInForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        fields = ['email', 'password']

