from django.urls import path

from . import views

app_name = "learn"
urlpatterns = [
    path("courses/", views.CourseIndex.as_view(), name="course-index"),
    path("courses/<str:code>/", views.Courses, name="course-overview"),
    path("courses/<str:code>/lessons", views.Lessons, name="lessons-overview"), # Lessons by Course
    path("<str:code>/", views.course_landing_page, name="course-landing_page"), #TODO is this redundant?
    path("courses/lesson/<str:quiz_slug>/", views.QuizLessons, name="quiz-lesson-page"),
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
