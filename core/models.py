from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    data = models.JSONField(default=dict)

    class Meta:
        db_table_comment = (
            "Profiles for learner tracking linked to django.contrib.auth.user"
        )

    def __str__(self):
        return self.user
