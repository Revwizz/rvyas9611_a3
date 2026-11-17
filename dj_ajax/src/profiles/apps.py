# FILE          : apps.py
# PROJECT       : SENG2045 - Assignment 3
# PROGRAMMER    : Ritik Vyas
# FIRST VERSION : 2026-11-14
# DESCRIPTION   : App configuration for the profiles app
# 

from django.apps import AppConfig

# CLASS       : ProfilesConfig
# DESCRIPTION : Settings for the profiles app, used by Django when it starts.
class ProfilesConfig(AppConfig):
    name = 'profiles'

    # FUNCTION    : ready
    # DESCRIPTION : Runs once when Django starts. Imports the signals file so
    #               a Profile is created automatically for every new user.
    # PARAMETERS  : none
    # RETURNS     : nothing
    def ready(self):
        import profiles.signals