# FILE          : views.py
# PROJECT       : SENG2045 - Assignment 3
# PROGRAMMER    : Ritik Vyas
# FIRST VERSION : 2026-11-14
# DESCRIPTION   : Views for the posts app. Shows the main page and detail page,
#                 and handles the Ajax requests for loading posts, creating,
#                 liking, updating and deleting posts, and uploading photos.
# 

from django.shortcuts import render
from .models import Post, Photo
from django.http import JsonResponse, HttpResponse
from .forms import PostForm
from profiles.models import Profile
from .utils import action_permission
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

def is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'

# Create your views here.

# FUNCTION    : post_list_and_create
# DESCRIPTION : Shows the main posts page with the create post form. When the
#               form is sent with Ajax and is valid, saves the new post with
#               the logged-in user as the author.
# PARAMETERS  : request : the HTTP request sent by the browser
# RETURNS     : JsonResponse with the new post's data, or the main page

@login_required
def post_list_and_create(request):
    form = PostForm(request.POST or None)
    # qs = Post.objects.all()

    if is_ajax(request):
        if form.is_valid():
            author = Profile.objects.get(user = request.user)
            instance = form.save(commit = False)
            instance.author = author
            instance.save()
            return JsonResponse({
                'title': instance.title,
                'body': instance.body,
                'author': instance.author.user.username,
                'id': instance.id
            })
    context = {
        'form': form,
    }

    return render(request, 'posts/main.html', context)

# FUNCTION    : post_detail
# DESCRIPTION : Shows the detail page for one post, with an empty form that
#               detail.js fills in for the update modal.
# PARAMETERS  : request : the HTTP request sent by the browser
#               pk      : the id of the post
# RETURNS     : the rendered detail page

@login_required
def post_detail(request, pk):
    obj = Post.objects.get(pk = pk)
    form = PostForm()

    context = {
        'obj': obj,
        'form': form,
    }

    return render(request, 'posts/detail.html', context)

# FUNCTION    : load_post_data_view
# DESCRIPTION : Sends a group of three posts for the main page. num_posts is
#               the total shown so far, so the slice gives the next three.
# PARAMETERS  : request   : the HTTP request sent by the browser
#               num_posts : how many posts should be shown after this request
# RETURNS     : JsonResponse with the posts' data and the total number of posts

@login_required
def load_post_data_view(request, num_posts):
    if is_ajax(request):
        visible = 3
        upper = num_posts
        lower = upper - visible
        size = Post.objects.all().count()

        qs = Post.objects.all()
        data = []
        for obj in qs:
            item = {
                'id': obj.id,
                'title': obj.title,
                'body': obj.body,
                'like': True if request.user in obj.liked.all() else False,
                'count': obj.like_count,
                'author': obj.author.user.username
            }
            data.append(item)
        return JsonResponse({'data' : data[lower : upper], 'size' : size})
    return redirect('posts:main-board')

# FUNCTION    : post_detail_data_view
# DESCRIPTION : Sends one post's data for the detail page, including the
#               author and the logged-in user, so detail.js can decide
#               whether to show the Update and Delete buttons.
# PARAMETERS  : request : the HTTP request sent by the browser
#               pk      : the id of the post
# RETURNS     : JsonResponse with the post's data,
#               otherwise a redirect to the main page

@login_required
def post_detail_data_view(request, pk):
    if is_ajax(request):
        obj = Post.objects.get(pk=pk)
        data = {
            'id': obj.id,
            'title': obj.title,
            'body': obj.body,
            'author': obj.author.user.username,
            'logged_in': request.user.username,
        }
        return JsonResponse({'data': data})
    return redirect('posts:main-board')

# FUNCTION    : like_unlike_post
# DESCRIPTION : Adds the logged-in user's like to a post, or removes it if
#               they already liked it.
# PARAMETERS  : request : the HTTP request, with the post's pk in POST data
# RETURNS     : JsonResponse with the new like state and like count

@login_required
def like_unlike_post(request):
    if is_ajax(request):
        pk = request.POST.get('pk')
        obj = Post.objects.get(pk = pk)
        if request.user in obj.liked.all():
            liked = False
            obj.liked.remove(request.user)
        else:
            liked = True
            obj.liked.add(request.user)
        return JsonResponse({'liked' : liked, 'count' : obj.like_count})
    return redirect('posts:main-board')

# FUNCTION    : update_post
# DESCRIPTION : Saves a new title and body for a post. Only the post's author
#               can do this
# PARAMETERS  : request : the HTTP request, with title and body in POST data
#               pk      : the id of the post
# RETURNS     : JsonResponse with the updated title and body

@login_required
@action_permission
def update_post(request, pk):

    obj = Post.objects.get(pk=pk)
    if is_ajax(request):
        new_title = request.POST.get('title')
        new_body = request.POST.get('body')
        obj.title = new_title
        obj.body = new_body
        obj.save()
    return JsonResponse({
        'title': new_title,
        'body': new_body,
    })

# FUNCTION    : delete_post
# DESCRIPTION : Deletes a post. Only the post's author can do this, 
#               and only through an Ajax request.
# PARAMETERS  : request : the HTTP request sent by the browser
#               pk      : the id of the post
# RETURNS     : JsonResponse with a short message

@login_required
@action_permission
def delete_post(request, pk):

    obj = Post.objects.get(pk=pk)
    if is_ajax(request):
        obj.delete()
        return JsonResponse({'msg' : 'some message'})
    return JsonResponse({'msg' : 'access denied - ajax only'})

# FUNCTION    : image_upload_view
# DESCRIPTION : Receives a photo uploaded by Dropzone and saves it as a Photo
#               linked to the newly created post.
# PARAMETERS  : request : the HTTP request, with the file and new_post_id
# RETURNS     : an empty HttpResponse

@login_required
def image_upload_view(request):

    if request.method == 'POST':
        img = request.FILES.get('file')
        new_post_id = request.POST.get('new_post_id')
        post = Post.objects.get(id = new_post_id)
        Photo.objects.create(image = img, post = post)
    return HttpResponse()