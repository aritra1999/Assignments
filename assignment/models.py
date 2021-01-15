from django.db import models
from django.contrib.auth.models import User

from Assignments.utls import slug_generator


class Class(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=11, blank=True, null=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    batch = models.CharField(max_length=50, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slug_generator()
            super(Class, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


class Assignment(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=11, blank=True, null=True)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True)
    due_date = models.DateTimeField(max_length=50, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    isActive = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slug_generator()
            super(Assignment, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


class Question(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=11, blank=True, null=True)
    added_by = models.ForeignKey(User, default="1", on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=True)
    body = models.TextField(max_length=5000, null=True, blank=True)
    input_format = models.TextField(max_length=1000, null=True, blank=True)
    output_format = models.TextField(max_length=1000, null=True, blank=True)
    allowed_lang = models.CharField(max_length=10, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slug_generator()
            super(Question, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.title)


class Submission(models.Model):
    submitted_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, null=True, on_delete=models.CASCADE)
    score = models.IntegerField(null=True, blank=True, default=0)
    lastRun = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    status = models.CharField(null=True, max_length=7, blank=True, default="Wrong")

    def __str__(self):
        return str(self.submitted_by)


class BestSubmission(models.Model):
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    score = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return str(self.submitted_by)


class Executions(models.Model):
    submission = models.OneToOneField(Submission, null=True, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    language = models.CharField(max_length=10, null=True, blank=True)
    verdict = models.CharField(max_length=10, null=True, blank=True)
    message = models.CharField(max_length=100, null=True, blank=True)
    time_taken = models.CharField(max_length=10, null=True, blank=True)
    mem_used = models.CharField(max_length=10, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.language)


class IO(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    input1 = models.TextField(null=True, blank=True)
    input2 = models.TextField(null=True, blank=True)
    input3 = models.TextField(null=True, blank=True)
    input4 = models.TextField(null=True, blank=True)
    input5 = models.TextField(null=True, blank=True)
    output1 = models.TextField(null=True, blank=True)
    output2 = models.TextField(null=True, blank=True)
    output3 = models.TextField(null=True, blank=True)
    output4 = models.TextField(null=True, blank=True)
    output5 = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=11, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slug_generator()
            super(IO, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.question)
