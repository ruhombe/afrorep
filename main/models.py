from django.db import models
from django.db import models
from django.utils.html import mark_safe
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.html import format_html
from django.urls import reverse
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from ckeditor.fields import RichTextField
from datetime import date

class Profiles(models.Model):
    user =  models.OneToOneField(User, on_delete=models.CASCADE,  null=True, blank=True, related_name="profile")
    profile_image = models.ImageField(blank=True, null=True, upload_to='images')
    first_name =  models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    user_name = models.CharField(max_length=200, null=True, blank=True)
    city =  models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    address = models.TextField(max_length=200,null=True, blank=True)
    website = models.URLField( null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user_name
    

    @property
    def imageURL(self):
        try:
            url = self.profile_image.url
        except:
            url = ''
        return url

    def image_tag(self):

        return mark_safe('<img src="{}" width="50" height="50"/>'.format(self.imageURL))
  
        image_tag.short_description = 'Image'


class SkillCategory(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Skills(models.Model):
    skill = models.CharField(max_length=200, null=True, blank=True)
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.skill} ({self.category})" if self.category else self.skill


class UserSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_skills")
    skill = models.ForeignKey(Skills, on_delete=models.CASCADE)
    date_selected = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.skill.skill}"


class About(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name="about")
    bio = models.TextField(max_length=5000, null=True, blank=True)

    def __str__(self):
        return self.user.username
    

class Experience(models.Model):
    user =  models.OneToOneField(User, on_delete=models.CASCADE,  null=True, blank=True, related_name="skills")
    position_title = models.CharField(max_length=200, null=True, blank=True)
    company = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(max_length=7000,null=True, blank=True)
    start_date = models.CharField(max_length=200,null=True, blank=True)
    end_date = models.CharField(max_length=200,null=True, blank=True)

    def __str__(self):
        return self.user.username

        
class Portfolio(models.Model):
    user =  models.OneToOneField(User, on_delete=models.CASCADE,  null=True, blank=True, related_name="portfolio")
    title = models.CharField(max_length=200, null=True, blank=True)
    description =models.TextField(max_length=4000,null=True, blank=True)
    image_one =  models.ImageField(blank=True, null=True, upload_to='images')
    image_two =  models.ImageField(blank=True, null=True, upload_to='images')
    image_three =  models.ImageField(blank=True, null=True, upload_to='images')
    image_four =  models.ImageField(blank=True, null=True, upload_to='images')

    def __str__(self):
        return self.user.username
