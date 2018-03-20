from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),

    url(r'^about$', views.blog_about, name='about'),
    url(r'^behavior-basics$', views.blog_behavior_basics, name='behavior_basics'),
    url(r'^research$', views.blog_research, name='research'),
    url(r'^resources$', views.blog_resources, name='resources'),
    url(r'^what-is-aba$', views.blog_what_is_aba, name='what-is-aba'),
]
