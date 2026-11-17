# FILE          : models.py
# PROJECT       : SENG2045 - Assignment 3
# PROGRAMMER    : Ritik Vyas
# FIRST VERSION : 2026-11-14
# DESCRIPTION   : Database model for the profiles app. Each user has one
#                 Profile with a bio and an avatar image.
# 

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# CLASS       : Profile
# DESCRIPTION : Extra information for a user: a bio and an avatar image.
#               Created automatically for each new user (see signals.py).
#               Uploaded avatars are saved in media/avatars/; users without
#               one get the default media/avatar.png.

class Profile(models.Model):
    user = models.OneToOneField (User, on_delete = models.CASCADE)
    bio = models.TextField (blank = True)
    avatar = models.ImageField (default = 'avatar.png', upload_to = 'avatars')
    updated = models.DateTimeField (auto_now = True)
    created = models.DateTimeField (auto_now_add = True)

    # FUNCTION    : __str__
    # DESCRIPTION : Text shown for a profile, for example in the admin site.
    # PARAMETERS  : none
    # RETURNS     : "profile of the user <username>"
    def __str__(self):
        return f"profile of the user {self.user.username}"