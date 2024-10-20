from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'fluency'
urlpatterns = [
    url(r'^$', views.fluency_index, name='index'),
    url(r'^(?P<quiz_id>\w+)/deck_(?P<deck_id>\w+)/$', views.fluency_view, name='fluency_view'),
    url(r'^(?P<quiz_id>\w+)/deck_(?P<deck_id>\w+)/timed/$', views.fluency_timed_view, name='fluency_timed_view'),
    url(r'^(?P<choice_id>\w+)/tally/$', views.tally_vote, name='tally_vote'),
    url(r'inspect/(?P<flashcard_id>\w+)/$', views.fluency_flashcard_inspector, name='fluency_flashcard_inspector'),
    url(r'score/$', views.submit_score_report, name='submit_score_report'),

]
