import datetime
from django.db import models
from django.utils import timezone

from django_ckeditor_5.fields import CKEditor5Field

from django.core.validators import validate_slug

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from quiz.models import Unit, Form, Choice, Question, Task, QuizScore, Form

from fluency.models import Deck


# Create your models here.
class Course(models.Model):
    course_name = models.CharField(max_length=50)
    course_description = RichTextField()
    course_target = models.CharField(max_length=50, default="RBT")
    course_units = models.ManyToManyField(Unit)

    def __str__(self):
        return self.course_name

    def get_course_description(self):
        return self.course_description

    def get_course_id(self):
        return self.course_id


class Objective(models.Model):
    objective_name = models.CharField(max_length=75, default="A")
    objective_short_name = models.CharField(max_length=75, blank=True, null=True)
    objective_description = RichTextField(null=True)
    objective_unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    objective_task_list_item = models.ManyToManyField(Task)

    def __str__(self):
        return self.objective_name

    def get_objective_unit(self):
        return self.objective_unit

    def get_objective_name(self):
        return self.objective_name

    def get_objective_id(self):
        return self.objective_id


class Certification(models.Model):
    certification_name = models.CharField(max_length=50)
    certification_description = RichTextField()

    def __str__(self):
        return self.certification_name

    def get_certification_description(self):
        return self.certification_description

    def get_certification_id(self):
        return self.certification_id


class LessonPage(models.Model):
    author = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, validators=[validate_slug])
    pic = models.CharField(max_length=200, null=True, blank=True)
    snippet_size = models.IntegerField(default=150)
    body = RichTextField()
    order = models.IntegerField()
    lesson_certification = models.ForeignKey(Certification, on_delete=models.CASCADE)
    lesson_course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson_unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    lesson_objectives = models.ManyToManyField(Objective)

    lesson_quizzes = models.ManyToManyField(Form, blank=True)

    last_lesson = models.ForeignKey(
        "self",
        related_name="last_lesson_page",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    next_lesson = models.ForeignKey(
        "self",
        related_name="next_lesson_page",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    # help text
    slug.help_text = "must be a single string, e.g. 'this-is-an-example'"
    pic.help_text = "This is the 'splash' picture that will be shown for the unit. You can leave it blank. FOR PICS SERVED UP ON THE SITE, THEY SHOULD START WITH /static/img/"
    snippet_size.help_text = "The snippet_size determines how much of a text to 'preview' before the card shows the 'study' button"

    STATUS_CHOICES = (
        ("d", "Draft"),
        ("p", "Published"),
        ("w", "Withdrawn"),
    )

    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    page_views = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Lesson Pages"

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Unit(models.Model):
    unit_name = models.CharField(max_length=50)
    unit_order = models.IntegerField(blank=True, null=True)
    unit_weight = models.IntegerField(blank=True, null=True)
    unit_description = RichTextField()
    unit_target = models.CharField(max_length=50, default="RBT")
    unit_lessons = models.ManyToManyField(LessonPage, blank=True)

    unit_weight.help_text = "should match how many questions are on the BACB's exam"

    def __str__(self):
        return self.unit_name

    def get_unit_description(self):
        return self.unit_description

    def get_unit_id(self):
        return self.unit_id


class TaskListItemCategory(models.Model):
    task_list_item_category_name = models.CharField(max_length=50)
    task_list_item_category_description = RichTextField()

    def __str__(self):
        return self.task_list_item_category_name

    def get_task_list_item_category_description(self):
        return self.task_list_item_category_description

    def get_task_list_item_category_id(self):
        return self.task_list_item_category_id

    class Meta:
        verbose_name_plural = "Task List Item Categories"


class TaskListItem(models.Model):
    task_list_item_name = models.CharField(max_length=50)
    task_list_item_description = RichTextField()

    def __str__(self):
        return self.task_list_item_name

    def get_task_list_item_description(self):
        return self.task_list_item_description

    def get_task_list_item_id(self):
        return self.task_list_item_id


# One-to-One link with django's user model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_lesson_course = models.ForeignKey(
        Course, on_delete=models.CASCADE, blank=True, null=True
    )
    last_lesson_page = models.ForeignKey(
        LessonPage, on_delete=models.CASCADE, blank=True, null=True
    )
    course_units_completed = models.ManyToManyField(Unit, blank=True)
    course_lessons_completed = models.ManyToManyField(
        LessonPage, related_name="course_lessons_completed", blank=True
    )
    user_quiz_forms_completed = models.ManyToManyField(Form, blank=True)
    user_fluency_decks_completed = models.ManyToManyField(Deck, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
