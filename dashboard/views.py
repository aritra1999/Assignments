import json
import requests
import asyncio
import aiohttp

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from accounts.models import Profile, Enrolled
from assignment.models import Question
from django.contrib.auth.models import User

from assignment.models import Assignment, Class, Submission


def home_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')

    context = {
        'title': 'Home'
    }

    return render(request, 'dashboard/home.html', context)


@login_required
def dashboard_view(request):
    user = request.user
    profile = Profile.objects.get(user=request.user)
    if profile.type == "teacher":
        if request.method == "POST":
            Class.objects.create(
                created_by=request.user,
                name=request.POST.get('class_name'),
                batch=request.POST.get('section'),
            )
        classInstances = Class.objects.filter(created_by=user)
        for classInstance in classInstances:
            classInstance.assignmentNumber = Assignment.objects.filter(class_name=classInstance).count()
            classInstance.studentNumber = Enrolled.objects.filter(class_name=classInstance).count()
        context = {
            'title': 'Dashboard',
            'user': request.user,
            'createdClass': classInstances,
            'profile': profile,
        }
        return render(request, 'dashboard/dashboard_teacher.html', context)
    elif user.profile.type == "student":
        if request.method == "POST":
            classSlug = request.POST.get('class_slug')
            classEnrolled = Class.objects.get(slug=classSlug)
            checkEnroll = Enrolled.objects.filter(class_name=Class.objects.get(slug=classSlug), student=request.user)
            if checkEnroll.count() == 0:
                instance = Enrolled.objects.create(
                    student=request.user,
                    class_name=classEnrolled,
                )
                instance.save()
                return redirect("/dashboard/class/" + classSlug)
            else:
                messages.info(request, 'Already present in the classroom!')
        context = {
            'title': 'Dashboard',
            'user': request.user,
            'profile': Profile.objects.get(user=request.user),
            'classes': Enrolled.objects.filter(student=request.user),
        }
        return render(request, 'dashboard/dashboard_student.html', context)


@login_required
def class_view(request, class_slug):
    user = request.user
    userType = Profile.objects.get(user=user)
    if userType.type == "student":
        classSelected = Class.objects.get(slug=class_slug)
        try:
            assignments = Assignment.objects.filter(class_name=classSelected, isActive=True)
        except:
            assignments = None
        context = {
            'title': 'Class',
            'assignments': assignments,
            'classSelected': classSelected,
            'profile': Profile.objects.get(user=request.user),
        }
        return render(request, 'dashboard/class.html', context)
    else:
        classSelected = Class.objects.get(slug=class_slug)
        assignmentNumber = Assignment.objects.filter(class_name=classSelected).count()
        assignmentsAll = Assignment.objects.filter(class_name=classSelected)
        studentNumber = Enrolled.objects.filter(class_name=classSelected).count()
        students = Enrolled.objects.filter(class_name=classSelected)
        classSelected = Class.objects.get(slug=class_slug)
        try:
            assignments = Assignment.objects.filter(class_name=classSelected)
        except:
            assignments = None
        for student in students:
            student.rollNo = (Profile.objects.get(user=student.student)).rollNo
        context = {
            'title': 'Class',
            'assignments': assignments,
            'classSelected': classSelected,
            'assignmentNumber': assignmentNumber,
            'studentNumber': studentNumber,
            'students': students,
            'assignmentsAll': assignmentsAll,
            'profile': Profile.objects.get(user=request.user),
        }
        return render(request, 'dashboard/class_teacher.html', context)


@login_required
def assignment_view(request, assignment_slug):
    user = request.user
    userType = Profile.objects.get(user=user)
    if userType.type == "student":
        assignmentSelected = Assignment.objects.get(slug=assignment_slug)
        try:
            questions = Question.objects.filter(assignment=assignmentSelected)
        except:
            questions = None
        context = {
            'title': 'Dashboard',
            'assignmentSelected': assignmentSelected,
            'questions': questions,
        }
        return render(request, 'dashboard/assignment.html', context)
    else:
        assignmentSelected = Assignment.objects.get(slug=assignment_slug)
        try:
            questions = Question.objects.filter(assignment=assignmentSelected)
        except:
            questions = None
        context = {
            'title': 'Dashboard',
            'assignmentSelected': assignmentSelected,
            'questions': questions,
        }
        return render(request, 'dashboard/assignment_teacher.html', context)


@login_required
def question_view(request, question_slug):
    question = Question.objects.get(slug=question_slug)
    context = {
        'title': 'Question',
        'question': question
    }
    return render(request, 'dashboard/question.html', context)


@login_required
def report_view(request, email):
    context = {
        'title': 'Report'
    }
    return render(request, 'dashboard/report.html', context)


@login_required
def submit(request, question_slug):
    if request.method == "POST":
        response = {}
        try:
            question = Question.objects.get(slug=question_slug)
        except:
            return JsonResponse({'error': 'Bad Request'})
        print(question)

        response['totalscore'] = 0
        for it in range(1, 6):
            input = open("media/io/" + question_slug + "_" + str(it) + ".in", "rt").read()
            output = open("media/io/" + question_slug + "_" + str(it) + ".out", "rt").read().strip()

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


@login_required
def assignment_create(request, class_slug):
    classSelected = Class.objects.get(slug=class_slug)
    print(classSelected)
    context = {
        'title': 'Create',
    }
    if request.method == "POST":
        newAssignment = Assignment.objects.create(
            created_by=request.user,
            class_name=classSelected,
            due_date=request.POST.get('assignmentDate'),
            name=request.POST.get('assignmentName'),
        )
        return redirect("/dashboard/assignment/" + newAssignment.slug)
    return render(request, 'dashboard/assignmentCreation.html', context)


@login_required
def question_create(request, assignment_slug):
    assignmentSelected = Assignment.objects.get(slug=assignment_slug)
    print(assignmentSelected)
    context = {
        'title': 'Add Questions',
    }
    if request.method == 'POST':
        Question.objects.create(
            assignment=assignmentSelected,
            added_by=request.user,
            title=request.POST.get('questionName'),
            body=request.POST.get('problemStatement'),
            input_format=request.POST.get('inputFormat'),
            output_format=request.POST.get('outputFormat'),
            allowed_lang=request.POST.get('allowedLang'),
        )
        return redirect("/dashboard/assignment/" + assignment_slug)
    return render(request, 'dashboard/questionCreate.html', context)


@login_required
def question_delete(request, question_slug, assignment_slug):
    questionSelected = Question.objects.get(slug=question_slug)
    questionSelected.delete()
    return redirect("/dashboard/assignment/" + assignment_slug)


@login_required
def remove_student(request, class_slug, student_email):
    student = Enrolled.objects.filter(class_name=Class.objects.get(slug=class_slug),
                                      student=User.objects.get(email=student_email))
    student.delete()
    return redirect("/dashboard/class/"+class_slug)


@login_required
def submissions_view(request, question_slug):
    user = request.user
    userType = Profile.objects.get(user=request.user)
    questionSelected = Question.objects.get(slug=question_slug)
    user = request.user
    print(userType.type)
    if userType.type == "student":
        try:
            submissionSelected = Submission.objects.filter(submitted_by=user, question=questionSelected)
        except:
            submissionSelected = None
        context = {
            'title': 'Submissions',
            'questionSelected': questionSelected,
            'submissionSelected': submissionSelected,
        }
        return render(request, 'dashboard/submissions.html', context)
    else:
        try:
            submissionSelected = Submission.objects.filter(question=questionSelected)
        except:
            submissionSelected = None
        print(submissionSelected)
        context = {
            'title': 'Submissions',
            'questionSelected': questionSelected,
            'submissionSelected': submissionSelected,
        }
        return render(request, 'dashboard/submission_teacher.html', context)


def join_view(request, class_slug):
    if request.user.is_authenticated:
        classSelected = Class.objects.get(slug=class_slug)
        user = request.user
        checkEnrollStatus = Enrolled.objects.filter(class_name=classSelected, student=user)
        if checkEnrollStatus.count() == 0:
            instance = Enrolled.objects.create(
                student=request.user,
                class_name=classSelected,
            )
            instance.save()
        return redirect("/dashboard/class/" + class_slug)
    else:
        nextUrl = "/dashboard/class/" + class_slug
        return redirect('/auth/signin')


def publish_assignment(request, assignment_slug):
    Assignment.objects.filter(slug=assignment_slug).update(isActive=True)
    return redirect("/dashboard/assignment/"+assignment_slug)


def deactivate_assignment(request, assignment_slug):
    Assignment.objects.filter(slug=assignment_slug).update(isActive=False)
    return redirect("/dashboard/assignment/"+assignment_slug)
