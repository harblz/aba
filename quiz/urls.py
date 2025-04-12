from django.urls import path
from . import views

app_name = "quiz"
urlpatterns = [
    path("<str:code>/<int:number>/start/", views._start, name="start-quiz"),
    path("quiz/next/", views._continue, name="continue"),
    path("quiz/save/", views._save_progress, name="save-progress"),
    path("quiz/check/", views._check_answer, name="check-answer"),
    path("<str:code>/", views.quizzes_by_course, name="quizzes-by-course"),
    path("<str:code>/<int:number>/", views.show_quiz, name="quiz"),
    path("", views.quiz_index, name="quizzes"),
]
