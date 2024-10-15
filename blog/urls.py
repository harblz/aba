from django.urls import path, include, re_path

import learn.urls
from . import views

app_name = "blog"
urlpatterns = [
<<<<<<< HEAD
    path("", views.posts.as_view(), name="blog-posts"),    
=======
    path("", views.posts, name="blog-posts"),
>>>>>>> refs/remotes/origin/develop
    path("<int:post_id>/", views.post, name="blog-post"),
]
