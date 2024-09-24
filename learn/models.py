from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.auth.models import User


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
    # Competencies and topics (e.g., BCBA, RBT)
    code = models.CharField(max_length=10, unique=True, primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)  # Content to be displayed on page
    content = models.OneToOneField("Pages", on_delete=models.RESTRICT)
    course_data = models.JSONField(default=dict)

    def __str__(self):
        return self.name

    def get_course_description(self):
        return self.description

    def get_course_id(self):
        return self.code

    def get_task_list(self) -> dict:
        if self.code == "RBT" or self.code == "BCBA" or self.code == "BCaBA":
            tasks = self.task_list.all().order_by("area", "task")
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
    def get_by_natural_key(self, license, area, task):
        return self.get(license=license, area=area, task=task)


class Task(models.Model):
    license = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="task_list"
    )
    area = models.CharField(max_length=1)
    area_name = models.CharField(max_length=50)
    task = models.IntegerField(max_length=2)
    task_desc = models.CharField(max_length=100)

    objects = TaskManager()

    def __str__(self):
        return f"{self.license} Task List: Item {self.area}-{self.task}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["license", "area", "task"], name="unique_tasks"
            )
        ]
        db_table_comment = "Tasks for RBT, BCaBA, and BCBA according to the BACB"
