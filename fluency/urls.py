from django.urls import path, include, re_path

from . import views

app_name = 'fluency'
urlpatterns = [
    re_path(r'^$', views.fluency_index, name='index'),
    re_path(r'^(?P<quiz_id>\w+)/deck_(?P<deck_id>\w+)/$', views.fluency_view, name='fluency_view'),
    re_path(r'^(?P<quiz_id>\w+)/deck_(?P<deck_id>\w+)/timed/$', views.fluency_timed_view, name='fluency_timed_view'),
    re_path(r'^(?P<choice_id>\w+)/tally/$', views.tally_vote, name='tally_vote'),
    re_path(r'inspect/(?P<flashcard_id>\w+)/$', views.fluency_flashcard_inspector, name='fluency_flashcard_inspector'),
    re_path(r'score/$', views.submit_score_report, name='submit_score_report'),
]
