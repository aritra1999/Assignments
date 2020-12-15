from django.urls import path

from .views import dashboard_view, class_view, question_view

urlpatterns = [
    path('', dashboard_view, name='assignments-home'),
    path('', dashboard_view, name='assignments-home'),
    path('', dashboard_view, name='assignments-home'),
]
