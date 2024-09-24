from django.db import models

from learn import models as learn


class Quiz(models.Model):
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
        return (self.course, self.number)

    class Meta:
        models.UniqueConstraint(fields=["topic", "number"], name="unique_quiz")
        db_table_comment = "Table of available quizzes"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    q_no = models.IntegerField("Question Number")
    text = models.TextField("Question Text")
    one = models.TextField("Question One")
    two = models.TextField("Question Two")
    three = models.TextField("Question Three")
    four = models.TextField("Question Four")
    answer = models.ForeignKey("self", on_delete=models.SET_NULL)
