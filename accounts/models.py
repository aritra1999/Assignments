from django.db import models
from django.contrib.auth.models import User

from assignment.models import Class


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=8, null=True, blank=True)
    university = models.CharField(max_length=8, null=True, blank=True)
    rollNo = models.CharField(max_length=7, null=True, blank=True)

    def __str__(self):
        return str(self.user.username)


class Enrolled(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    class_name = models.OneToOneField(Class, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.student)
