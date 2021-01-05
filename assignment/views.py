from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages

from accounts.models import Enrolled
from .models import Class

@login_required
def join_view(request, class_slug):
    try:
        Enrolled.objects.create(
            user=request.user
            class_name=Class.objects.get(slug=class_slug)
        ).save()    
        messages.add_message(request, "Enrolled")
    except: 
        messages.add_message(request, "Error Occured")
    # Access using {{ message }}
    return redirect('/dashboard')


