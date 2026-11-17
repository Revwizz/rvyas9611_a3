# FILE          : admin.py
# PROJECT       : SENG2045 - Assignment 3
# PROGRAMMER    : Ritik Vyas
# FIRST VERSION : 2026-11-14
# DESCRIPTION   : Registers the Post and Photo models with the Django admin site,
#                 so posts and their photos can be viewed, added, edited and
#                 deleted from /admin.
# 
from django.contrib import admin
from .models import Post, Photo

# Register your models here.

admin.site.register(Post)
admin.site.register(Photo)