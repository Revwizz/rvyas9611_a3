# FILE          : views.py
# PROJECT       : SENG2045 - Assignment 3
# PROGRAMMER    : Ritik Vyas
# FIRST VERSION : 2026-11-16
# DESCRIPTION   : Views for the profiles app. Shows the My Profile page and
#                 saves the updated bio and avatar sent with Ajax.
#
from django.shortcuts import render
from .models import Profile
from .forms import ProfileForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

# Create your views here.

def is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'

# FUNCTION    : my_profile_view
# DESCRIPTION : Shows the logged-in user's profile page with the profile form.
#               When the form is sent with Ajax and is valid, saves the new
#               bio and avatar.
# PARAMETERS  : request : the HTTP request sent by the browser
# RETURNS     : JsonResponse with the updated bio, avatar URL and username,
#               otherwise the rendered profile page

@login_required
def my_profile_view(request):
    obj = Profile.objects.get(user = request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance = obj)
    if is_ajax(request):
        if form.is_valid():
            instance = form.save()
            return JsonResponse({
                'bio': instance.bio,
                'avatar': instance.avatar.url,
                'user': instance.user.username
            })
    context = {
        'obj': obj,
        'form': form,
    }

    return render(request, 'profiles/main.html', context)