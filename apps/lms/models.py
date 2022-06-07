from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    name = models.CharField(max_length=255)
    teacher = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='teaching_groups')
    students = models.ManyToManyField(User, related_name='studying_groups')

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    group = models.ForeignKey(Group, on_delete=models.PROTECT, null=True,
                              related_name='lessons')

    def __str__(self):
        return self.name
