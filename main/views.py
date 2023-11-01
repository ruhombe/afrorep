from django.shortcuts import render, redirect
#from .models import
from django.db.models import Q
#from .forms import SearchForm, CreateUserForm
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


def home(request):
    context={}
    return render(request, 'home.html', context)