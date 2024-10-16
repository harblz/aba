from django.urls import path

from . import views

app_name = "learn"
urlpatterns = [
    path("courses/", views.CourseIndex.as_view(), name="course-index"),
    path("<str:code>/", views.course_landing_page, name="course-landing_page"),
    path(
        "<str:code>/tasklist/",
        views.TaskListView.as_view(),
        name="tasklist-landing-page",
    ),
    path("<str:code>/course/", views.lesson_page, name="lesson-page"),
    path(
        "task/change/options",
        views.task_changeform_options,
        name="task-changeform-options",
    ),
    path("task/change/area_name", views.get_area_name, name="get-area-name"),
]
