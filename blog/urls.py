from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),

    url(r'^research$', views.blog_research, name='research'),
    url(r'^coffee$', views.blog_coffee, name='coffee'),
    url(r"^blog_coffee_checkout$", views.blog_coffee_checkout, name="blog_coffee_checkout")
]
