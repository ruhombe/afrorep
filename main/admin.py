from django.contrib import admin
from django.utils.safestring import mark_safe
from django.contrib import admin
from .models import  Profiles, Portfolio, UserSkill,Skills, SkillCategory, About, Experience, Review, PortfolioImages
from django_mptt_admin.admin import DjangoMpttAdmin
from mptt.admin import DraggableMPTTAdmin
from django.utils.html import format_html
#from .forms import
from .forms import PortfolioImagesForm
from django.forms import inlineformset_factory


admin.site.register(Profiles)
admin.site.register(SkillCategory)
admin.site.register(Skills)
admin.site.register(UserSkill)



ProductImageFormSet = inlineformset_factory(Portfolio, PortfolioImages, form=PortfolioImagesForm, extra=4)
class PortfolioImagesInline(admin.TabularInline):
    model = PortfolioImages
    form = PortfolioImagesForm
    extra = 5
    fields = ('image', 'image_tag')
    readonly_fields = ('image_tag',)
    def image_tag(self, obj):
        return mark_safe('<img src="{}" width="50" height="50"/>'.format(obj.imageURL))
    image_tag.short_description = 'Image'
    list_display = ('image', 'image_tag',)


class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'image_tag']
    readonly_fields=('image_tag',)
    inlines = [PortfolioImagesInline]
    def image_tag(self, obj):
        return mark_safe('<img src="{}" width="50" height="50"/>'.format(obj.imageURL))
    image_tag.short_description = 'Image'


admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(About)
admin.site.register(Experience)
admin.site.register(Review)
