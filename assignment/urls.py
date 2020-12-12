from django.urls import path

from .views import assignments_home_view

urlpatterns = [
    path('', assignments_home_view, name='assignments-home'),
]
