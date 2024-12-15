from django.db import models
from django.conf import settings

from learn import models as learn
from django_ckeditor_5.fields import CKEditor5Field


class Quiz(models.Model):
    slug = models.SlugField(unique=True, primary_key=True)
    course = models.ForeignKey(learn.Course, on_delete=models.CASCADE)
    areas = models.ManyToManyField(learn.ContentArea, blank=True)
    number = models.IntegerField(default=1)
    desc = models.CharField("Description", max_length=100)
    timed = models.BooleanField("Timed?", default=False, null=True, blank=True)
    time = models.DurationField("Time in minutes", null=True, blank=True)

    class Meta:
        models.UniqueConstraint(fields=["course", "number"], name="unique_quiz")
        db_table_comment = "Table of available quizzes"
        verbose_name_plural = "Quizzes"
        default_related_name = "quizzes"

    def __str__(self):
        return f"{self.course} Quiz #{self.number}"

    def save(self, *args, **kwargs):
        if not self.slug and self._state.adding:
            try:
                previous = Quiz.objects.filter(course=self.course.code).latest("number")
            except Quiz.DoesNotExist:
                previous = None

            if not previous:
                self.number = 1
            else:
                self.number = previous.number + 1
            self.slug = f"{self.course.code}-{self.number}"
        super(Quiz, self).save(*args, **kwargs)

    def natural_key(self):
        return self.course.code, self.number


class BaseQuestion(models.Model):
    category = models.ForeignKey(learn.ContentArea, on_delete=models.CASCADE)
    text = CKEditor5Field("Question Text")
    hint = CKEditor5Field("Question Hint", blank=True, null=True)
    disabled = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.text


class MultipleChoiceQuestion(BaseQuestion):
    answer = models.OneToOneField(
        "MultipleChoiceAnswer", on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        default_related_name = "multiple_choice_questions"
        verbose_name = "Multiple Choice Question"
        db_table_comment = "All multiple choice questions"


class TrueFalseQuestion(BaseQuestion):
    answer = models.BooleanField()

    class Meta:
        default_related_name = "true_false_questions"
        verbose_name = "True/False Question"
        db_table_comment = "All True/False Questions"


class MultipleChoiceAnswer(models.Model):
    question = models.ForeignKey(MultipleChoiceQuestion, on_delete=models.CASCADE)
    text = models.TextField("Answer Text")

    class Meta:
        default_related_name = "answers"
        db_table_comment = "Table of multiple choice answers"

    def __str__(self):
        return self.text


class QuizProgress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    session = models.CharField(max_length=100)
    quiz = models.SlugField(unique=True, primary_key=True)
    index = models.IntegerField(default=0)
    timed = models.BooleanField("Timed?", default=False, null=True, blank=True)
    time = models.DurationField("Time in minutes", null=True, blank=True)
    key = models.JSONField(default=dict)

    class Meta:
        db_table_comment = "Quiz progress data"
