from django import forms
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
#from .models import 

class CreateUserForm(UserCreationForm):
    phone = forms.CharField()
    country = forms.CharField()
    address = forms.CharField()
    class Meta:
        model = User
        fields = ['first_name','last_name', 'username',  'email', 'country', 'phone', 'address', 'password1', 'password2']
