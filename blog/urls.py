from django.urls import path

from . import views

app_name = "blog"
urlpatterns = [
    path("", views.posts, name="blog-posts"),
    path("<int:post_id>/", views.view_post, name="blog-post"),
]
