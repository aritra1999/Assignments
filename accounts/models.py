from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=8, null=True, blank=True)
    university = models.CharField(max_length=8, null=True, blank=True)

    def __str__(self):
        return str(self.user.username)