from django.urls import path

from . import views

app_name = "learn"
urlpatterns = [
    path("courses/", views.CourseIndex.as_view(), name="course_index"),
    path("<str:code>/", views.course_landing_page, name="course_landing_page"),
    path(
        "<str:code>/tasklist/",
        views.TaskListView.as_view(),
        name="tasklist_landing_page",
    ),
    path("<str:code>/lesson/", views.lesson_page, name="lesson_page"),
]
