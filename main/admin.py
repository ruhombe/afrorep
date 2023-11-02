from django.contrib import admin
from django.utils.safestring import mark_safe
from django.contrib import admin
from .models import  Profiles
from django_mptt_admin.admin import DjangoMpttAdmin
from mptt.admin import DraggableMPTTAdmin
from django.utils.html import format_html
#from .forms import
from django.forms import inlineformset_factory


admin.site.register(Profiles)
