from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/$', views.post_details_by_id, name='post_details_by_id'),
    url(r'^get/post/(?P<pk>\d+)/$', views.get_post_by_id, name='post_details_by_id'),
    path('<slug:slug>', views.post_details_by_slug, name='post_details_by_slug'),
    url(r'^research$', views.blog_research, name='research'),
    url(r'^coffee$', views.blog_coffee, name='coffee'),
    url(r"^blog_coffee_checkout$", views.blog_coffee_checkout, name="blog_coffee_checkout")
]
