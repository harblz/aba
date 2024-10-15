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
    path("<str:code>/course/", views.lesson_page, name="lesson_page"),
    path(
        "task/change/options",
        views.task_changeform_options,
        name="task_changeform_options",
    ),
    path("task/change/area_name", views.get_area_name, name="get_area_name"),
]
