from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'learn'
urlpatterns = [
    url(r'^$', views.course_index, name='course_index'),
    url(r'account/$', views.course_account, name='course_account'),
    #url(r'^(?P<quiz_id>\w+)/deck_(?P<deck_id>\w+)/$', views.fluency_view, name='fluency_view'),
]
