from django.urls import path

from .views import (
    dashboard_view,
    class_view,
    question_view,
    report_view,
    assignment_view,
    submit,
    assignment_create,
    question_create,
    question_delete,
    remove_student,
    submissions_view,
    publish_assignment,
    deactivate_assignment,
    remove_class,
    remove_assignment,
    student_details,
)

urlpatterns = [
    path('', dashboard_view, name='dash'),
    path('class/<class_slug>', class_view, name='class'),
    path('assignment/<assignment_slug>', assignment_view, name='assignment'),
    path('question/<question_slug>', question_view, name='question'),
    path('report/<email>', report_view, name='report'),
    path('submit/<question_slug>', submit, name='submit'),
    path('create/<class_slug>', assignment_create, name='assignmentCreate'),
    path('create/questions/<assignment_slug>', question_create, name='questionCreate'),
    path('questions/delete/<assignment_slug>/<question_slug>', question_delete, name='questionDelete'),
    path('class/remove/<class_slug>/<student_email>', remove_student, name='removeStudent'),
    path('submissions/<question_slug>', submissions_view, name='submission'),
    path('assignment/active/<assignment_slug>', publish_assignment, name='activate'),
    path('assignment/deactivate/<assignment_slug>', deactivate_assignment, name='deactivate'),
    path('class/remove/<class_slug>', remove_class, name="removeClass"),
    path('assignment/remove/<class_slug>/<assignment_slug>', remove_assignment, name="removeAssignment"),
    path('student/<class_slug>/<student_email>', student_details, name='studentDetails'),
]
