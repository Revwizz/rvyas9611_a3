# FILE          : admin.py
# PROJECT       : SENG2045 - Assignment 3
# PROGRAMMER    : Ritik Vyas
# FIRST VERSION : 2026-11-14
# DESCRIPTION   : Registers the Profile model with the Django admin site, so
#                 user profiles can be viewed and edited from /admin.
# 
from django.contrib import admin
from .models import Profile

# Register your models here.

admin.site.register(Profile)