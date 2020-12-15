from django.shortcuts import render


def home_view(request):
    context = {
        'title': 'Home'

    }
    return render(request, 'dashboard/home.html', context)


def dashboard_view(request):
    context = {
        'title': 'Dashboard'
    }
    return render(request, 'dashboard/dashboard_student.html', context)



