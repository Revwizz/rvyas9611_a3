# FILE          : utils.py
# PROJECT       : SENG2045 - Assignment 3
# PROGRAMMER    : Ritik Vyas
# FIRST VERSION : 2026-11-16
# DESCRIPTION   : Custom decorator that makes sure only the author of a post
#                 can update or delete it.
#
from .models import Post
from profiles.models import Profile
from django.http import HttpResponse

# FUNCTION    : action_permission
# DESCRIPTION : Decorator for the update and delete views. Before the view runs,
#               it checks that the logged-in user is the author of the post.
#               If they are, the view runs normally; if not, access is denied.
# PARAMETERS  : func : the view function being protected
# RETURNS     : wrapper : a new function that does the check, then calls func

def action_permission(func):
    # FUNCTION    : wrapper
    # DESCRIPTION : Finds the logged-in user's profile and the post from the URL,
    #               then compares the post's author with the user.
    # PARAMETERS  : request : the HTTP request sent by the browser
    #               kwargs  : values from the URL, including the post's pk
    # RETURNS     : the view's response if the user is the author,
    #               otherwise an "access denied" HttpResponse
    def wrapper(request, **kwargs):
        pk = kwargs.get('pk')
        profile = Profile.objects.get(user = request.user)
        post = Post.objects.get(pk = pk)
        if profile.user == post.author.user:
            print('yes')
            return func(request, **kwargs)
        else:
            print('no')
            return HttpResponse('access denied - you are not authorize')
        
    return wrapper