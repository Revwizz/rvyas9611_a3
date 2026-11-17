# FILE          : forms.py
# PROJECT       : SENG2045 - Assignment 3
# PROGRAMMER    : Ritik Vyas
# FIRST VERSION : 2026-11-14
# DESCRIPTION   : Form used to create and update posts. It is shown in the
#                 create post modal on the main page and in the update modal
#                 on the detail page.
#
from django import forms 
from .models import Post

# CLASS       : PostForm
# DESCRIPTION : A ModelForm built from the Post model. Only the title and body
#               fields are shown; the author, likes and dates are set by the
#               views and the model instead of by the user.

class PostForm(forms.ModelForm):
    # title = forms.CharField(widget = forms.TextInput(attrs = {'class:' : 'form-control'}))
    # body = forms.CharField(widget = forms.Textarea(attrs = {'class' : 'form-control', 'rows' : 3}))
    class Meta:
        model = Post
        fields = ('title', 'body',)