from django.urls import path, include, re_path

from . import views

app_name = "quiz"
urlpatterns = [
    path("", views.QuizIndex.as_view(), name="quizzes"),
    path("<str:code>/", views.IndexByCourse.as_view(), name="quizzes_by_course"),
    path("<str:code>/<int:number>/", views.get_quiz, name="get_quiz"),
    path("<str:code>/<int:number>/start/", views._start_quiz, name="start_quiz"),
    path("quiz/next/<int:question_id>/", views._next_question, name="next_question"),
    path("quiz/save/", views._save_progress, name="save_progress"),
]
