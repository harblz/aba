#from django.conf.urls import url
from django.urls import path, include, re_path

from . import views

urlpatterns = [
    
    re_path(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    re_path(r'^post/new/$', views.post_new, name='post_new'),
    re_path(r'^post/(?P<pk>\d+)/$', views.post_details_by_id, name='post_details_by_id'),
    re_path(r'^get/post/(?P<pk>\d+)/$', views.get_post_by_id, name='post_details_by_id'),
    path('<slug:slug>', views.post_details_by_slug, name='post_details_by_slug'),
    re_path(r'^research$', views.blog_research, name='research'),
    re_path(r'^coffee$', views.blog_coffee, name='coffee'),
    re_path(r"^blog_coffee_checkout$", views.blog_coffee_checkout, name="blog_coffee_checkout"),
    re_path(r"^thanks$", views.thanks, name="thanks")
]
