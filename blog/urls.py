from django.urls import path, include, re_path

import learn.urls
from . import views

app_name = "blog"
urlpatterns = [
    path("", views.posts, name="blog-posts"),
    path("<int:post_id>/", views.post, name="blog-post"),
]
