import json
import requests
import asyncio
import aiohttp

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from accounts.models import Profile, Enrolled
from assignment.models import Question


def home_view(request):
    if request.user.is_authenticated:
        redirect('/dashboard/')

    context = {
        'title': 'Home'
    }

    return render(request, 'dashboard/home.html', context)


@login_required
def dashboard_view(request):
    context = {
        'title': 'Dashboard',
        'user': request.user,
        'profile': Profile.objects.get(user=request.user),
    }

    # user = request.user
    # profile = Profile.objects.get()
    #
    # if profile.type == "teacher":
    #     return render(request, 'dashboard/dashboard_teacher.html', context)
    # elif profile.type == "student":
    context['classes'] = Enrolled.objects.filter(student=request.user)
    return render(request, 'dashboard/dashboard_student.html', context)


@login_required
def class_view(request, class_slug):
    context = {
        'title': 'Class'
    }
    return render(request, 'dashboard/class.html', context)


def assignment_view(request, assignment_slug):
    context = {
        'title': 'Dashboard'
    }
    return render(request, 'dashboard/assignment.html', context)


def question_view(request, question_slug):
    question = Question.objects.get(slug=question_slug)
    context = {
        'title': 'Question',
        'question': question
    }
    return render(request, 'dashboard/question.html', context)


def report_view(request, email):
    context = {
        'title': 'Report'
    }
    return render(request, 'dashboard/report.html', context)



def submit(request, question_slug):
    if request.method == "POST":
        response = {}
        question = Question.objects.get(slug=question_slug)
        print(question)

        response['totalscore'] = 0
        for it in range(1, 6):
            input = open("media/io/" + question_slug + "_" + str(it) + ".in", "rt").read()
            output = open("media/io/"+ question_slug + "_" + str(it) + ".out", "rt").read().strip()

            payload = {
                "language": question.allowed_lang,
                "code": request.POST.get('code'),
                "input": input
            }

            url = "https://nvdk5lgoek.execute-api.ap-south-1.amazonaws.com/JustRunStage"
            r = json.loads(requests.post(url, data=json.dumps(payload)).text)

            if r['verdict'] == "error":
                return JsonResponse({
                    'status': 'error',
                    'error': r
                })

            response['status'] = "success"
            response['time' + str(it)] = r['time']
            response['memory' + str(it)] = r['memory']

            if r['output'].strip() == output:
                response['verdict' + str(it)] = "correct"
                response['score' + str(it)] = "20"
                response['totalscore'] += 20
            else:
                response['verdict' + str(it)] = "wrong"

        print(response)
        return JsonResponse(response)
    else:
        return JsonResponse({'error': 'Bad Request'})

