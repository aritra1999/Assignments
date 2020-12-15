from django.urls import path

from .views import dashboard_view, class_view, question_view, report_view, assignment_view

urlpatterns = [
    path('', dashboard_view, name='dash'),
]
