from django.shortcuts import render, redirect
from .models import Profiles
from django.db.models import Q
from .forms import CreateUserForm
# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
import json
from django.db.models.signals import post_delete
from django.dispatch import receiver
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm,PasswordResetForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
#from .utils import 
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username= form.cleaned_data.get('username')
            phone= form.cleaned_data.get('phone')
            address = form.cleaned_data.get('address')
            country =form.cleaned_data.get('country').lower()
            #create customer
            Profiles.objects.create(user=user,phone=phone, country=country, address=address, name=username, email=user.email)
            user = authenticate(username=username, password=form.cleaned_data.get('password1'))
            if user is not None:
                login(request, user)
            messages.success(request, 'Customer account created for ' + username)
            return redirect('home') 
        else:
            messages.info( request, 'Make sure to follow the form field requirements')
     
    context={'form':form}
    return render(request, 'register.html', context) 


def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'username or password is  incorrect')
    context={}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):
    context={}
    return render(request, 'home.html', context)