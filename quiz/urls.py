#from django.conf.urls import url
from django.urls import path, include, re_path

from . import views

app_name = 'quiz'
urlpatterns = [
    re_path(r'^$', views.quiz_index, name='index'),
    re_path(r'^(?P<quiz_id>\w+)/form_(?P<form_id>\w+)/$', views.quiz_view, name='quiz'),
    re_path(r'^(?P<quiz_id>\w+)/form_(?P<form_id>\w+)/grade_question$', views.quiz_view, name='quiz'),
    re_path(r'inspect/(?P<question_id>\w+)/$', views.quiz_question_inspector, name='quiz_question_inspector'),
    re_path(r'score/$', views.submit_score_report, name='submit_score_report'),
]
