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

class Profiles(models.Model):
    user =  models.OneToOneField(User, on_delete=models.CASCADE,  null=True, blank=True, related_name="profile")
    profile_image = models.ImageField(blank=True, null=True, upload_to='images')
    first_name =  models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    user_name = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    address = models.TextField(max_length=200,null=True, blank=True)
    def __str__(self):
        return self.user_name
    
    
    
    
