from django.urls import path
from . import views

app_name = "quiz"
urlpatterns = [
    path("", views.QuizIndex.as_view(), name="quizzes"),
    path("<str:code>/", views.IndexByCourse.as_view(), name="quizzes_by_course"),
    path("<str:code>/<int:number>/", views.show_quiz, name="quiz"),
    path("<str:code>/<int:number>/start/", views._start, name="start_quiz"),
    path("quiz/next/", views._continue, name="continue"),
    path("quiz/save/", views._save_progress, name="save_progress"),
]
