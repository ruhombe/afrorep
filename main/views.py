from django.shortcuts import render, redirect
from .models import Profiles,Portfolio,SkillCategory,Skills,UserSkill,About,Experience
from django.db.models import Q
from .forms import CreateUserForm, ProfileForm, PortfolioForm # Create your views here.
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
from django.contrib.auth.models import User
##  amin username: afro
## password: Afrorep14

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            user = form.save()
            photo=form.cleaned_data.get('photo')
            username= form.cleaned_data.get('username')
            phone= form.cleaned_data.get('phone')
            address = form.cleaned_data.get('address')
            country =form.cleaned_data.get('country').lower()
            #create User Profile
            Profiles.objects.create(user=user,phone=phone,first_name=user.first_name, last_name=user.last_name, country=country, address=address, profile_image=photo, user_name=username, email=user.email)
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




@login_required
def update_profile(request,id):
    user = request.user
    profile = Profiles.objects.get(id=id)
    #portfolio = Portfolio.objects.get(id=id)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    if form.is_valid():
        profile=form.save(commit=False)
        user.first_name = profile.first_name
        user.last_name = profile.last_name
        user.username = profile.user_name
        user.email = profile.email
        user.save()
        profile.save()
        context={'form':form,}
        return redirect('home')
    else:
        messages.info(request, ' Sorry!! Something went wrong')
        context={'form':form}

    skill_categories = SkillCategory.objects.all()
    context={'form':form,  'user':user, 'skill_categories':skill_categories}
    return render(request, 'profile.html', context)






def home(request):
    #skill_categories = SkillCategory.objects.all()

    context = {}
    return render(request, 'home.html', context)





@login_required
def handle_skill_selection(request):
    if request.method == 'POST':
        selected_skill_ids = request.POST.getlist('selected_skills')
        user = request.user  # Assuming the user is logged in
        # Add selected skills to the user
        for skill_id in selected_skill_ids:
            skill = Skills.objects.get(id=skill_id)
            UserSkill.objects.create(user=user, skill=skill)
        return redirect('home')  # Redirect to the user's profile or another page
    else:
        return redirect('home')  #