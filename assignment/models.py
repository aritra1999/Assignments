from django.db import models
from django.contrib.auth.models import User


class Class(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class Assignment(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=10, blank=True, null=True)
    class_name =  models.ForeignKey(Class, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True)
    due_date = models.DateField(max_length=50, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class Question(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=10, blank=True, null=True)
    title = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=5000, null=True, blank=True)
    allowed_lang = models.CharField(max_length=10, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)


class Submission(models.Model):
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    slug = models.SlugField(max_length=10, blank=True, null=True)
    score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.slug)


class BestSubmission(models.Model):
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    slug = models.SlugField(max_length=10, blank=True, null=True)
    score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.slug)


class Executions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    language = models.CharField(max_length=10, null=True, blank=True)
    verdict = models.CharField(max_length=10, null=True, blank=True)
    message = models.CharField(max_length=100, null=True, blank=True)
    time_taken = models.CharField(max_length=10, null=True, blank=True)
    mem_used = models.CharField(max_length=10, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.language)