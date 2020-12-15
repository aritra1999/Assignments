from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import signin_view, signup_view

urlpatterns = [
    path('signin/', signin_view, name='login_view'),
    path('signup/', signup_view, name='register_view'),
    path('logout/', LogoutView.as_view(), name="logout"),
]
