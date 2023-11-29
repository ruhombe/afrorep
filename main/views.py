from django.shortcuts import render, redirect
from .models import Profiles,Portfolio,SkillCategory,Skills,UserSkill,About,Experience,Review, PortfolioImages
from django.db.models import Q
from .forms import CreateUserForm, ProfileForm, PortfolioForm,ReviewForm , AboutForm, PortfolioImagesFormSet, ExperienceForm # Create your views here.
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
####################################################REGISTRATION AND LOGIN
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
######################################################################END REGISTRATION AND LOGIN

@login_required
def update_user_profile(request, id):
    user = request.user
    print(user)
    profile = Profiles.objects.get(user=user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    abouts= About.objects.get(user=user)
    about_form = AboutForm(request.POST or None, request.FILES or None, instance=abouts)
    experiences = Experience.objects.filter(user=user)
    portfolios=Portfolio.objects.filter(user=user)
    experience_form = ExperienceForm()
    portfolio_form = PortfolioForm()
    image_formset = PortfolioImagesFormSet()
    if request.method == 'POST':
        #save portfolio data
        if "profile" in request.POST:
            if form.is_valid():
                profile = form.save(commit=False)
                user.first_name = profile.first_name
                user.last_name = profile.last_name
                user.username = profile.user_name
                user.email = profile.email
                user.save()
                profile.save()
                messages.success(request, 'Profile updated successfully')
                return redirect('profile', id=profile.user.id)
            else:
                messages.error(request, 'Sorry!! Something went wrong. Try again')
        #update or create about data
        elif 'about' in request.POST:
            if about_form.is_valid():
                about_form.save()
                messages.success(request, 'About info updated successfully')
                return redirect('profile', id=profile.user.id)
            else:
                messages.error(request, 'Sorry!! Something went wrong. Try again')
        ##save experience data 
        elif 'experience' in request.POST:
            experience_form=ExperienceForm(request.POST)
            if experience_form.is_valid():
                position_data = experience_form.cleaned_data.get('position_title')
                company_data = experience_form.cleaned_data.get('company')
                description_data = experience_form.cleaned_data.get('description')
                start_date_data = experience_form.cleaned_data.get('start_date')
                end_date_data = experience_form.cleaned_data.get('end_date')
                experience = experience_form.save(commit=False)
                experience.user = request.user
                experience.position_title = position_data
                experience.company = company_data
                experience.description = description_data
                experience.start_date = start_date_data
                experience.end_date = end_date_data
                experience.save()
                messages.success(request, 'Experience Added successfully')
                return redirect('profile', id=profile.user.id)
            else:  
                messages.error(request, 'Sorry!! Something went wrong. Try again')
        #save portfolio data:
        elif 'portfolio' in request.POST:
            portfolio_form = PortfolioForm(request.POST or None, request.FILES or None)
            image_formset = PortfolioImagesFormSet(request.POST or None, request.FILES or None)
            if portfolio_form.is_valid() and image_formset.is_valid(): 
                port = portfolio_form.save(commit=False)
                port.user=request.user
                port.save()
                image_formset.instance=port
                image_formset.save()
                messages.success(request, 'Portfolio Added successfully')
                return redirect('profile', id=profile.user.id)
        else:
            messages.success(request, 'invalid submition!')
            print("dindt save")
            return redirect('profile', id=profile.user.id)
    skill_categories = SkillCategory.objects.all()
    context = {'form': form, 'user': user, 'portfolios':portfolios, 'portfolio_form':portfolio_form, 'portfolio_image_formset':image_formset, 'about_form':about_form,'experiences':experiences, 'experience_form':experience_form, 'skill_categories': skill_categories}
    return render(request, 'update_profile.html', context)


def user_profile(request, id):
    user = get_object_or_404(User, id=id)
    review_form = ReviewForm()
    try:
        profile = Profiles.objects.get(user=user)
       
        skill_categories = SkillCategory.objects.all()
        user_skills = UserSkill.objects.filter(user=user)
        chosen_categories = set(user_skill.skill.category for user_skill in user_skills)
        about_user = About.objects.filter(user=user)
        user_experience = Experience.objects.filter(user=user)
        user_portfolio = Portfolio.objects.filter(user=user)
        extra_images=[]
        for portfolio in user_portfolio:
            extra_images = PortfolioImages.objects.filter(portfolio=portfolio)
        user_reviews = Review.objects.filter(target_user=user)
        if request.method == "POST":
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                text_data = review_form.cleaned_data.get('text')
                rating_data = review_form.cleaned_data.get('rating')
                reviewer_data = request.user
                target_user_id = review_form.cleaned_data.get('target_user')
                target_user_data = get_object_or_404(User, id=target_user_id)
                review = review_form.save(commit=False)
                review.reviewer=reviewer_data
                review.target_user =target_user_data
                review.text=text_data
                review.rating=rating_data
                review.save()
                return redirect('profile', id=target_user_id)
            else:
                return JsonResponse({'error': 'Ooops! Something went wrong!'}, status=400)
        context = {'user': user, 'about_user':about_user,'extra_images':extra_images, 'review_form':review_form,'user_portfolio':user_portfolio, 'user_reviews':user_reviews, 'user_experience':user_experience, 'profile': profile, 'skill_categories': skill_categories, 'user_skills':user_skills, 'chosen_categories':chosen_categories}
        return render(request, 'profile.html', context)
    except Profiles.DoesNotExist:
        return render(request, 'profile_not_found.html')


def home(request):
    profiles = User.objects.all()
    context = {'profiles': profiles}
    return render(request, 'home.html', context)

############################################################select skill
@login_required
def handle_skill_selection(request):
    if request.method == 'POST':
        selected_skill_ids = request.POST.getlist('selected_skills')
        user = request.user
        profile= Profiles.objects.get(user=user)
        for skill_id in selected_skill_ids:
            skill = Skills.objects.get(id=skill_id)
            UserSkill.objects.create(user=user, skill=skill)
        messages.success(request, 'Skill Added successfully')
        return redirect('profile', id=profile.user.id) #for now
    else:
        messages.success(request, 'Skill not saved! Something went wrong')
   
########################################################################return  reviews given to user
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


###################DELETE A SKILL
def delete_user_skill(request, skill_id):
    user=request.user
    user_skill = get_object_or_404(UserSkill, id=skill_id)
    profile= Profiles.objects.get(user=user)
    if user_skill.user == request.user:
        user_skill.delete()
        messages.success(request, 'Experience Deleted successfully')
        return redirect('profile', id=profile.user.id) 
    else:
        messages.success(request, 'Skill Deleted successfully')
        return redirect('profile', id=profile.user.id) 

##################delete experience
def delete_user_experience(request, experience_id):
    user=request.user
    user_experience = get_object_or_404(Experience, id=experience_id)
    profile= Profiles.objects.get(user=user)
    if user_experience.user == request.user:
        user_experience.delete()
        messages.success(request, 'Experience Deleted successfully')
        return redirect('profile', id=profile.user.id) 
    else:
        messages.success(request, 'Experience Deleted successfully')
        return redirect('profile', id=profile.user.id) 
    
###########################delete portfolio
def delete_user_portfolio(request, portfolio_id):
    user= request.user
    user_portfolio = get_object_or_404(Portfolio, id=portfolio_id)
    profile= Profiles.objects.get(user=user)
    if user_portfolio.user == request.user:
        user_portfolio.delete()
        messages.success(request, 'Portfolio Deleted successfully')
        return redirect('profile', id=profile.user.id) 
    else:
        messages.success(request, 'Unauthorized')
        return redirect('profile', id=profile.user.id) 
        #return JsonResponse({'error': 'Unauthorized'}, status=403)