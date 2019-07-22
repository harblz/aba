from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'learn'
urlpatterns = [
    url(r'^$', views.course_index, name='course_index'),
    url(r'account/$', views.course_account, name='course_account'),
    url(r'unit/(?P<pk>\d+)', views.unit_landing_page, name='unit_landing_page'),
    path('topic/<slug:slug>/', views.topic_page),
    #url(r'^(?P<quiz_id>\w+)/deck_(?P<deck_id>\w+)/$', views.fluency_view, name='fluency_view'),
]
