# from django.conf.urls import url
from django.urls import path, include, re_path

from . import views

app_name = "quiz"
urlpatterns = [
    path("", views.QuizIndex.as_view(), name="quizzes"),
    path("<str:course>/", views.IndexByCourse.as_view(), name="quizzes_by_course"),
    path("<str:course>/<int:quiz>/", views.get_quiz, name="get_quiz"),
    path("<str:course>/<int:quiz>/start/", views._start_quiz, name="start_quiz"),
    path("quiz/next/<int:quiz_id>/", views._next_question, name="next_quiz"),
    path("quiz/save/", views._save_progress, name="save_progress"),
]
