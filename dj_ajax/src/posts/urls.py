# FILE          : urls.py
# PROJECT       : SENG2045 - Assignment 3
# PROGRAMMER    : Ritik Vyas
# FIRST VERSION : 2026-11-14
# DESCRIPTION   : URL routes for the posts app. Connects each address to its
#                 view: the main page, loading posts, likes, photo uploads,
#                 and the detail, update and delete pages for a post.
#

from django.urls import path
from .views import (
    post_list_and_create,
    load_post_data_view,

    like_unlike_post,
    post_detail,
    post_detail_data_view,
    delete_post,
    update_post,
    image_upload_view,
)

app_name = 'posts'

urlpatterns = [
    # Main page: list of posts and the create post form
    path('', post_list_and_create, name = 'main-board'),

    #like or unlike a post
    path('like-unlike/', like_unlike_post, name = 'like-unlike'),

    # photo uploads from Dropzone
    path('upload/', image_upload_view, name = 'image-upload'),

    # Detail page for one post
    path('<pk>/', post_detail, name = 'post-detail'),

    # update a post's title and body
    path('<pk>/update/', update_post, name = 'post-update'),

    # delete post
    path('<pk>/delete/', delete_post, name = 'post-delete'),

    # get the next group of posts for the main page
    path('data/<int:num_posts>/', load_post_data_view, name = 'posts-data'),

    # get one post's data for the detail page
    path('<pk>/data/', post_detail_data_view, name = 'post-detail-data'),
]