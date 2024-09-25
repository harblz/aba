from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import HStoreField

from django_ckeditor_5.fields import CKEditor5Field


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # JSONField for all three maybe?
    # scores = Should relate to quiz field for score tracking
    # progress = Should store progress in fluency
    # current_lesson = Should store current/incomplete fluency lesson

    def __str__(self):
        return self.user

    class Meta:
        db_table_comment = (
            "Profiles for learner tracking linked to django.contrib.auth.user"
        )


class Course(models.Model):
    """Competencies, subjects, and topics (e.g., BCBA, RBT, Feeding Therapy, etc.)"""

    # TODO: Add relation in pages
    code = models.CharField(max_length=10, unique=True, primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)  # Content to be displayed on page
    weights = HStoreField("# of questions per category")
    course_data = models.JSONField()

    def __str__(self):
        return self.name

    def get_course_description(self) -> str:
        """Returns the full description of the course"""
        return self.description

    def natural_key(self) -> str:
        """Returns the acronym/code for the competency"""
        return self.code

    def get_task_list(self) -> dict:
        """Returns the entire BACB Task List for RBTs, BCBAs, or BCaBAs"""
        if self.code == "RBT" or self.code == "BCBA" or self.code == "BCaBA":
            tasks = self.tasks.filter(code=self.code).order_by("area", "task")
            task_list = {}
            for task in tasks:
                task_name = f"{task.area}-{task.task}"
                task_list[task_name] = task.task_desc
            return task_list
        else:
            pass

    class Meta:
        db_table_comment = "The competency, license, or topic of interest"


class TaskManager(models.Manager):
    """Manager to return natural key of Task"""

    def get_by_natural_key(self, license, area, task):
        return self.get(license=license, area=area, task=task)


class Task(models.Model):
    """BACB Task List items"""

    license = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="tasks")
    area = models.CharField(max_length=1)
    area_name = models.CharField(max_length=50)
    task = models.IntegerField()
    task_desc = models.CharField(max_length=100)

    objects = TaskManager()

    def __str__(self):
        return f"{self.license} Task List: Item {self.area}-{self.task}"

    def natural_key(self):
        return (self.license, self.area, self.task)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["license", "area", "task"], name="unique_tasks"
            )
        ]
        db_table_comment = "Tasks for RBT, BCaBA, and BCBA according to the BACB"


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    page = models.IntegerField()
    title = models.CharField(max_length=100)
    content = CKEditor5Field()

    def __str__(self):
        return f"{self.course} Lesson {self.page}"

    class Meta:
        models.UniqueConstraint(fields=["course", "page"], name="unique_lessons")
        db_table_comment = "Lesson pages for each course"
