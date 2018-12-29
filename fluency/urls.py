from django.conf.urls import url

from . import views

app_name = 'fluency'
urlpatterns = [
    url(r'^$', views.fluency_index, name='index'),
    url(r'^(?P<quiz_id>\w+)/deck_(?P<deck_id>\w+)/$', views.fluency_view, name='fluency_view'),
    url(r'^(?P<quiz_id>\w+)/deck_(?P<deck_id>\w+)/timed/$', views.fluency_timed_view, name='fluency_timed_view'),
]
