from django.urls import path

from . import views

app_name = "learn"
urlpatterns = [
    path("courses/", views.course_index, name="course_index"),
    path("<str: code>/", views.course_landing_page, name="course_landing_page"),
    path(
        "<str: code>/tasklist/",
        views.return_task_list,
        name="tasklist_landing_page",
    ),
    path("<str: code>/<int: page>/", views.lesson_page, name="lesson_page"),
]
