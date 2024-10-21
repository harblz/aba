from django.db import models

from learn import models as learn


class Quiz(models.Model):
    slug = models.SlugField(unique=True, primary_key=True)
    course = models.ForeignKey(learn.Course, on_delete=models.CASCADE)
    areas = models.ManyToManyField(learn.ContentArea, blank=True, null=True)
    number = models.IntegerField(default=1)
    desc = models.CharField("Description", max_length=100)
    timed = models.BooleanField("Timed?", default=False)
    time = models.IntegerField("Time in minutes", default=0, null=True, blank=True)

    class Meta:
        models.UniqueConstraint(fields=["course", "number"], name="unique_quiz")
        db_table_comment = "Table of available quizzes"
        verbose_name_plural = "Quizzes"
        default_related_name = "quizzes"

    def __str__(self):
        return f"{self.course} Quiz #{self.number}"

    def save(self, *args, **kwargs):
        self.slug = f"{self.course.code}-{self.number}"
        super(Quiz, self).save(*args, **kwargs)

    def natural_key(self):
        return (self.course.code, self.number)


class Question(models.Model):
    category = models.ForeignKey(learn.ContentArea, on_delete=models.CASCADE)
    text = models.TextField("Question Text", unique=True)
    one = models.TextField("Question One")
    two = models.TextField("Question Two")
    three = models.TextField("Question Three", null=True, blank=True)
    four = models.TextField("Question Four", null=True, blank=True)
    answer = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        db_table_comment = "Table of all questions from any quiz"
        default_related_name = "questions"

    def __str__(self):
        return self.text
