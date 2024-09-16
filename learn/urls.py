from django.urls import path, include, re_path

from . import views

app_name = 'learn'
urlpatterns = [
    re_path(r'^$', views.course_index, name='course_index'),
    re_path(r'account/$', views.course_account, name='course_account'),
    re_path(r'unit/(?P<pk>\d+)', views.unit_landing_page, name='unit_landing_page'),
    path('topic/<slug:slug>/', views.topic_page),
    #re_path(r'^(?P<quiz_id>\w+)/deck_(?P<deck_id>\w+)/$', views.fluency_view, name='fluency_view'),
]
