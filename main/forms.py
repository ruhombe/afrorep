from django import forms
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from .models import Profiles, Portfolio, Experience, About ,Review

class CreateUserForm(UserCreationForm):
    photo = forms.ImageField()
    phone = forms.CharField()
    country = forms.CharField()
    address = forms.CharField()
    class Meta:
        model = User
        fields = ['first_name','last_name', 'photo', 'username',  'email', 'country', 'phone', 'password1', 'password2']



class ProfileForm(UserChangeForm):
    class Meta:
        model = Profiles
        fields= '__all__'

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = '__all__'

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields='__all__'

class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = '__all__'


class ReviewForm(forms.ModelForm):
    target_user = forms.IntegerField(widget=forms.HiddenInput())
    class Meta:
        model = Review
        fields = ['text', 'rating']
        