from django.db import models

from learn import models as learn


class Quiz(models.Model):
    slug = models.SlugField(unique=True, primary_key=True)
    course = models.ForeignKey(learn.Course, on_delete=models.CASCADE)
    number = models.IntegerField(default=0)
    questions = models.IntegerField("Number of Questions", default=0)
    desc = models.CharField("Description", max_length=100)
    timed = models.BooleanField("Timed?", default=False)
    time = models.IntegerField("Time in minutes", default=0, null=True, blank=True)
    has_list = models.BooleanField("Has a task list?", default=False)

    def __str__(self):
        return f"{self.course} Quiz #{self.number}"

    def natural_keY(self):
        return (self.course.code, self.number)

    class Meta:
        models.UniqueConstraint(fields=["course", "number"], name="unique_quiz")
        db_table_comment = "Table of available quizzes"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    category = models.CharField("Category", max_length=1, null=True, blank=True)
    text = models.TextField("Question Text", unique=True)
    one = models.TextField("Question One")
    two = models.TextField("Question Two")
    three = models.TextField("Question Three", null=True, blank=True)
    four = models.TextField("Question Four", null=True, blank=True)
    answer = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.text

    class Meta:
        db_table_comment = "Table of all questions from any quiz"
