from django.contrib import admin

from .models import Class, Assignment, Question, Submission, BestSubmission, Executions

admin.site.register(Class)
admin.site.register(Assignment)
admin.site.register(Question)
admin.site.register(Submission)
admin.site.register(BestSubmission)
admin.site.register(Executions)
