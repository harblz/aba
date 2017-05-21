from django.conf.urls import url

from . import views

app_name = 'quiz'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^hello/', views.home, name='home'),
    url(r'^(?P<pk>[0-9]+)/\w+', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<quiz_name>\w+)/$', views.quiz_view, name='quiz'),
    url(r'^(?P<quiz_name>)/create_post', views.home, name='home'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
