# FILE          : urls.py
# PROJECT       : SENG2045 - Assignment 3
# PROGRAMMER    : Ritik Vyas
# FIRST VERSION : 2026-11-16
# DESCRIPTION   : URL routes for the profiles app. Connects the My Profile
#                 address to its view.
# 

from django.urls import path
from .views import my_profile_view

# namespace
app_name = 'profiles'

urlpatterns = [
    path ('my/', my_profile_view, name = 'my-profile'),
]
