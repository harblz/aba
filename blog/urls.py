from django.urls import path, include, re_path

from . import views

urlpatterns = [
    path("", views.posts.as_view(), name="blog-posts"),    
    path("<int:post_id>/", views.post, name="blog-post"),
]