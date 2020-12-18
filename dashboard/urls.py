from django.urls import path

from .views import (
    dashboard_view,
    class_view,
    question_view,
    report_view,
    assignment_view
)

urlpatterns = [
    path('', dashboard_view, name='dash'),
    path('class/<class_slug>', class_view, name='class'),
    path('assignment/<assignment_slug>', assignment_view, name='assignment'),
    path('question/<question_slug>', question_view, name='question'),
    path('report/<email>', report_view, name='report'),
]
