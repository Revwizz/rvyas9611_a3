# FILE          : signals.py
# PROJECT       : SENG2045 - Assignment 3
# PROGRAMMER    : Ritik Vyas
# FIRST VERSION : 2026-11-14
# DESCRIPTION   : Signal that creates a Profile automatically whenever a new
#                 user is created
# 

from .models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# FUNCTION    : post_save_create_profile
# DESCRIPTION : Runs every time a User is saved. If the user was just created,
#               creates an empty Profile for them.
# PARAMETERS  : sender   : the model that sent the signal
#               instance : the User object that was saved
#               created  : True if this save created a new user
#               args, kwargs : extra values Django sends with the signal
# RETURNS     : nothing

@receiver(post_save, sender = User)
def post_save_create_profile(sender, instance, created, * args, **kwargs):
    print(sender)
    print(instance)
    print(created)
    if created:
        Profile.objects.create(user = instance)