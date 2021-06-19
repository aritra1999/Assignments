from django.contrib import admin
from django.urls import path, include

from dashboard.views import home_view, join_view, about_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('about/', about_view, name='about'),
    path('dashboard/', include('dashboard.urls')),
    path('auth/', include('accounts.urls')),
    path('assignments/', include('assignment.urls')),
    path('join/<class_slug>', join_view, name='join'),
]
