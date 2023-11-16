from django.shortcuts import render, redirect
from .models import Profiles,Portfolio,SkillCategory,Skills,UserSkill,About,Experience,Review
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
            country =form.cleaned_data.get('country').lower()
            #create User Profile
            Profiles.objects.create(user=user,phone=phone,first_name=user.first_name, last_name=user.last_name, country=country, profile_image=photo, user_name=username, email=user.email)
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



#@login_required
#def update_profile(request, id):
#    user = get_object_or_404(User, id=id)
#    profile = Profiles.objects.get(id=id)
#    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)

#    if request.method == 'POST':
#        if form.is_valid():
#            profile = form.save(commit=False)
#            user.first_name = profile.first_name
#            user.last_name = profile.last_name
#            user.username = profile.user_name
#            user.email = profile.email
#            user.save()
#            profile.save()
#            messages.success(request, 'Profile updated successfully')
#            return redirect('home')
#        else:
#            messages.error(request, 'Sorry!! Something went wrong')

#    skill_categories = SkillCategory.objects.all()
#    context = {'form': form, 'user': user, 'skill_categories': skill_categories}
#    return render(request, 'profile.html', context)

def user_profile(request, id):
    user = get_object_or_404(User, id=id)
    try:
        profile = Profiles.objects.get(user=user)
        skill_categories = SkillCategory.objects.all()
        user_skills = UserSkill.objects.filter(user=user)
        chosen_categories = set(user_skill.skill.category for user_skill in user_skills)
        about_user = About.objects.filter(user=user)
        user_experience = Experience.objects.filter(user=user)
        context = {'user': user, 'about_user':about_user, 'user_experience':user_experience, 'profile': profile, 'skill_categories': skill_categories, 'user_skills':user_skills, 'chosen_categories':chosen_categories}
        return render(request, 'profile.html', context)
    except Profiles.DoesNotExist:
        # Handle the case where the user has no profile
        return render(request, 'profile_not_found.html')






def home(request):
    profiles = User.objects.all()
    context = {'profiles': profiles}
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
    


def get_reviews_for_user(username):
    user = get_object_or_404(User, username=username)

    reviews = Review.objects.filter(target_user=user)

    reviews_data = []

    for review in reviews:
        reviewer_name = f"{review.reviewer.first_name} {review.reviewer.last_name}"
        reviews_data.append({
            'reviewer_name': reviewer_name,
            'text': review.text,
            'rating': review.rating,
            'created_at': review.created_at,
        })

    return reviews_data