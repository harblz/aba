from django.conf.urls import url

from . import views

app_name = 'quiz'
urlpatterns = [
    url(r'^$', views.quiz_index, name='index'),
    url(r'^(?P<quiz_id>\w+)/$', views.quiz_view, name='quiz'),
    url(r'^(?P<quiz_id>\w+)/form_(?P<form_id>\w+)/$', views.quiz_view, name='quiz'),
    url(r'^(?P<quiz_id>\w+)/form_(?P<form_id>\w+)/grade_question$', views.quiz_view, name='quiz'),
]
