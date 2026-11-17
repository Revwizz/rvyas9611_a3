# FILE          : forms.py
# PROJECT       : SENG2045 - Assignment 3
# PROGRAMMER    : Ritik Vyas
# FIRST VERSION : 2026-11-16
# DESCRIPTION   : Form used on the My Profile page to update the user's bio
#                 and avatar.
#

from django import forms
from .models import Profile

# CLASS       : ProfileForm
# DESCRIPTION : A ModelForm built from the Profile model. Only the bio and
#               avatar fields are shown; the user is set automatically.
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'avatar')