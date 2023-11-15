from django.contrib import admin
from django.utils.safestring import mark_safe
from django.contrib import admin
from .models import  Profiles, Portfolio, UserSkill,Skills, SkillCategory, About, Experience
from django_mptt_admin.admin import DjangoMpttAdmin
from mptt.admin import DraggableMPTTAdmin
from django.utils.html import format_html
#from .forms import
from django.forms import inlineformset_factory


admin.site.register(Profiles)
admin.site.register(SkillCategory)
admin.site.register(Skills)
admin.site.register(UserSkill)
admin.site.register(Portfolio)
admin.site.register(About)
admin.site.register(Experience)
