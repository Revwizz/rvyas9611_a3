# FILE          : models.py
# PROJECT       : SENG2045 - Assignment 3
# PROGRAMMER    : Ritik Vyas
# FIRST VERSION : 2026-11-14
# DESCRIPTION   : Database models for the posts app. A Post has a title, body,
#                 author and likes, a Photo is an image attached to a Post.
# 

from django.db import models
from django.contrib.auth.models import User
from profiles.models import Profile

# Create your models here.

# CLASS       : Post
# DESCRIPTION : A post written by a user. Stores the title, body, the author's
#               profile, the users who liked it, and when it was created and
#               last updated. Newest posts come first.

class Post (models.Model):
    title = models.CharField (max_length = 200)
    body = models.TextField()
    liked = models.ManyToManyField (User, blank = True)
    author = models.ForeignKey(Profile, on_delete = models.CASCADE)
    updated = models.DateTimeField (auto_now = True)
    created = models.DateTimeField (auto_now_add = True)

    # FUNCTION    : __str__
    # DESCRIPTION : Text shown for a post, for example in the admin site.
    # PARAMETERS  : none
    # RETURNS     : the post's title

    def __str__(self):
        return str(self.title)

    # FUNCTION    : like_count
    # DESCRIPTION : Counts how many users liked this post. Used like a field
    #               (post.like_count) because of @property.
    # PARAMETERS  : none
    # RETURNS     : the number of likes as an integer
    @property
    def like_count(self):
        return self.liked.all().count()

    # FUNCTION    : get_photos
    # DESCRIPTION : Gets all photos attached to this post, for the carousel
    #               on the detail page.
    # PARAMETERS  : none
    # RETURNS     : a queryset of the post's Photo objects
    def get_photos(self):
        return self.photo_set.all()

    class Meta:
        ordering = ("-created",)

# CLASS       : Photo
# DESCRIPTION : An image uploaded for a post (through Dropzone). Images are
#               saved in media/photos/. Deleting a post deletes its photos.
class Photo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="photos")
    created = models.DateTimeField(auto_now_add=True)

    # FUNCTION    : __str__
    # DESCRIPTION : Text shown for a photo, for example in the admin site.
    # PARAMETERS  : none
    # RETURNS     : the post's title and the photo's id
    def __str__(self):
        return f"{self.post.title}-{self.pk}"