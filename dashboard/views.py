import json
import requests

from django.http import JsonResponse
from django.shortcuts import render

from accounts.models import Profile


def home_view(request):
    context = {
        'title': 'Home'
    }

    return render(request, 'dashboard/home.html', context)


def dashboard_view(request):
    context = {
        'title': 'Dashboard'
    }
    # user = request.user
    # profile = Profile.objects.get()
    #
    # if profile.type == "teacher":
    #     return render(request, 'dashboard/dashboard_teacher.html', context)
    # elif profile.type == "student":
    return render(request, 'dashboard/dashboard_student.html', context)


def assignment_view(request):
    context = {
        'title': 'Dashboard'
    }
    return render(request, 'dashboard/assignment.html', context)


def class_view(request):
    context = {
        'title': 'Class'
    }
    return render(request, 'dashboard/class.html', context)


def question_view(request):
    context = {
        'title': 'Question'
    }
    return render(request, 'dashboard/question.html', context)


def report_view(request):
    context = {
        'title': 'Report'
    }
    return render(request, 'dashboard/report.html', context)


def submit(request):
    if request.method == "POST":
        payload = {
            "language": request.POST.get('language'),
            "code": request.POST.get('code'),
            "input": request.POST.get('input')
        }
        url = "https://nvdk5lgoek.execute-api.ap-south-1.amazonaws.com/JustRunStage"
        r = json.loads(requests.post(url, data=json.dumps(payload)).text)

        # verdict = r['verdict']
        # message = r['message']
        # output = r['output']
        # time = r['time']
        # memory = r['memory']

        response = {
            'response': r
        }
        return JsonResponse(response)
    else:
        return JsonResponse({'error': 'Bad Request'})
