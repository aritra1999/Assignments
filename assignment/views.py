from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# @login_required
def assignments_home_view(request):
    context = {
        'title': 'Assignments'
    }
    return render(request, 'assignments/home.html', context)
