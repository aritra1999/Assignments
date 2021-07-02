import json
import requests
import re
from django.contrib.auth import authenticate
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

from accounts.models import Profile, Enrolled
from assignment.models import Question, Assignment, Class, Submission, BestSubmission, IO


def home_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')

    context = {
        'title': 'Home'
    }

    return render(request, 'dashboard/home.html', context)


def about_view(request):
    context = {
        'title': 'About'
    }

    return render(request, 'dashboard/about.html', context)


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
            classInstance.assignmentNumber = Assignment.objects.filter(class_name=classInstance, isActive=True).count()
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
            assignments = Assignment.objects.filter(class_name=classSelected, isActive=True).order_by('-timestamp')
            assignmentCount = Assignment.objects.filter(class_name=classSelected, isActive=True).count()
            students = Enrolled.objects.filter(class_name=classSelected)
        except:
            assignments = None
            students = None
            assignmentCount = 0
        for student in students:
            student.rollNo = (Profile.objects.get(user=student.student)).rollNo
        context = {
            'title': 'Class',
            'assignments': assignments,
            'assignmentCount': assignmentCount,
            'classSelected': classSelected,
            'profile': Profile.objects.get(user=request.user),
            'students': students,
            'userType': userType,
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
            assignments = Assignment.objects.filter(class_name=classSelected).order_by('-timestamp')
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
        for question in questions:
            try:
                question.score = (BestSubmission.objects.get(submitted_by=user, question=question)).score
            except:
                question.score = 0
            try:
                question.lastRun = (Submission.objects.get(submitted_by=user, question=question)).lastRun
            except:
                question.lastRun = None
            try:
                passSubs = Submission.objects.filter(status="Passed", submitted_by=user, question=question).count()
                totalSubs = Submission.objects.filter(submitted_by=user, question=question).count()
                question.SR = int((passSubs/totalSubs)*100)
                print(question.SR)
            except:
                question.SR = 0
            try:
                if (BestSubmission.objects.get(submitted_by=user, question=question)).score > 40:
                    question.verdict = "Passed"
                else:
                    question.verdict = "Failed"
            except:
                question.verdict = "Submission Not Found"
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
        for question in questions:
            question.totalBestSub = (BestSubmission.objects.filter(question=question)).count()
            bestScoreSum = BestSubmission.objects.filter(question=question).aggregate(Sum('score')).get('score__sum', 0.00)
            try:
                question.averageScore = bestScoreSum / question.totalBestSub
            except:
                question.averageScore = 0
        context = {
            'title': 'Dashboard',
            'assignmentSelected': assignmentSelected,
            'questions': questions,
        }
        return render(request, 'dashboard/assignment_teacher.html', context)


@login_required
def question_view(request, question_slug):
    user = request.user
    profile = Profile.objects.get(user=user)
    if profile.type == "student":
        question = Question.objects.get(slug=question_slug)
        timeup = False
        if question.assignment.due_date < timezone.now():
            timeup = True
        
        
        context = {
            'title': 'Question',
            'question': question,
            'timeup': timeup
        }
        return render(request, 'dashboard/question.html', context)
    else:
        question = Question.objects.get(slug=question_slug)
        ios = IO.objects.filter(question=question)
        if request.method == "POST":
            Question.objects.filter(slug=question_slug).update(
                title=request.POST.get('questionName'),
                allowed_lang=request.POST.get('allowedLang'),
                input_format=request.POST.get('inputFormat'),
                body=request.POST.get('problemStatement'),
                output_format=request.POST.get('outputFormat')
            )
            ios.delete()            
            for testCase in range(1, int(request.POST.get('testCases')) + 1):
                IO.objects.create(
                    question=question,
                    input=request.POST.get('input' + str(testCase)),
                    output=request.POST.get('output' + str(testCase)),
                    score=request.POST.get('score' + str(testCase)),
                )
            return redirect("/dashboard/assignment/" + question.assignment.slug)
        context = {
            'title': 'Question',
            'question': question,
            'ios': ios,
        }
        return render(request, 'dashboard/question_teacher.html', context)


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

        io = IO.objects.get(question=question).__dict__

        response['totalscore'] = 0
        for it in range(1, 6):
            
            input = io['input' + str(it)]
            output = io['output' + str(it)]

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


            # check_output = re.sub('/^[ A-Za-z0-9_@./#&+-]*$/', '', r['output'].strip())
            # output = re.sub('/^[ A-Za-z0-9_@./#&+-]*$/', '', str(output).strip())
            check_output = r['output'].strip().replace('\n', '')
            output = output.strip().replace('\n', '')

            print(check_output, len(check_output))
            print(output, len(output))

            if check_output == output:
                response['verdict' + str(it)] = "Passed"
                response['score' + str(it)] = "20"
                response['totalscore'] += 20
            else:
                response['verdict' + str(it)] = "Failed"
            print("\n-------------------------\n")




        if response['totalscore'] < 40:
            response['verdict'] = "Failed"
        else:
            response['verdict'] = "Passed"

        timeup = False
        if question.assignment.due_date >= timezone.now():
            timeup = True
            Submission.objects.create(
                submitted_by=request.user,
                question=question,
                code=request.POST.get('code'),
                score=response['totalscore'],
                activity=request.POST.get('activity'),
                status=response['verdict'],
            )
            try:
                best = BestSubmission.objects.get(
                    submitted_by=request.user,
                    question=question
                )
                if response['totalscore'] > best.score:
                    print('Updating')
                    best.score = response['totalscore']
                    best.save()
            except:
                BestSubmission.objects.create(
                    submitted_by=request.user,
                    question=question,
                    score=response['totalscore']
                )
        return JsonResponse(response)
    else:
        return JsonResponse({'error': 'Bad Request'})


def run(request, question_slug):
    if request.method == "POST":
        response = {}
        try:
            question = Question.objects.get(slug=question_slug)
        except:
            return JsonResponse({'error': 'Bad Request'})

        io = IO.objects.get(question=question)

        input = io.input1
        output = io.output1

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
        response['time'] = r['time']
        response['memory'] = r['memory']

        if r['output'].strip() == output:
            response['verdict'] = "Passed"
        else:
            response['verdict'] = "Failed"

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
        question = Question.objects.create(
            assignment=assignmentSelected,
            added_by=request.user,
            title=request.POST.get('questionName'),
            body=request.POST.get('problemStatement'),
            input_format=request.POST.get('inputFormat'),
            output_format=request.POST.get('outputFormat'),
            allowed_lang=request.POST.get('allowedLang'),
        )
        
        for testCase in range(1, int(request.POST.get('testCases')) + 1):
            IO.objects.create(
                question=question,
                input=request.POST.get('input' + str(testCase)),
                output=request.POST.get('output' + str(testCase)),
                score=request.POST.get('score' + str(testCase)),
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
    return redirect("/dashboard/class/" + class_slug)


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
            submissionSelected = BestSubmission.objects.filter(question=questionSelected)
        except:
            submissionSelected = None
        print(submissionSelected)
        context = {
            'title': 'Submissions',
            'questionSelected': questionSelected,
            'submissionSelected': submissionSelected,
        }
        return render(request, 'dashboard/submission_teacher.html', context)


@login_required
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


@login_required
def publish_assignment(request, assignment_slug):
    Assignment.objects.filter(slug=assignment_slug).update(isActive=True)
    return redirect("/dashboard/assignment/" + assignment_slug)


@login_required
def deactivate_assignment(request, assignment_slug):
    Assignment.objects.filter(slug=assignment_slug).update(isActive=False)
    return redirect("/dashboard/assignment/" + assignment_slug)


@login_required
def remove_class(request, class_slug):
    classSelected = Class.objects.get(created_by=request.user, slug=class_slug)
    classSelected.delete()
    return redirect("/dashboard")


@login_required
def remove_assignment(request, assignment_slug, class_slug):
    removeAssignment = Assignment.objects.filter(created_by=request.user, slug=assignment_slug)
    removeAssignment.delete()
    return redirect("/dashboard/class/" + class_slug)


@login_required
def student_details(request, class_slug, student_email):
    user = request.user
    userType = Profile.objects.get(user=user).type
    studentSelected = User.objects.get(email=student_email)
    studentProfile = Profile.objects.get(user=studentSelected)
    classSelected = Class.objects.get(slug=class_slug)
    if userType == "teacher":
        context = {
            'title': 'Details',
            'studentSelected': studentSelected,
            'studentProfile': studentProfile,
        }
        return render(request, 'dashboard/studentDetails.html', context)
    else:
        return HttpResponse("Hello Student")


@login_required
def profile_view(request):
    context = {
        'title': 'Profile',
        'user': request.user,
    }
    if request.method == "POST":
        if request.POST.get('formName') == "nameChange":
            newFirstName = request.POST.get('firstName')
            newLastName = request.POST.get('lastName')
            User.objects.filter(id=request.user.id).update(first_name=newFirstName, last_name=newLastName)
            return redirect('/dashboard/profile')
        elif request.POST.get('formName') == "passwordChange":
            user = authenticate(request, username=request.user.username, password=request.POST.get('currPass'))
            if user is not None:
                newPass = request.POST.get('newPassword')
                newPassCnf = request.POST.get('newPasswordRep')
                if newPass == newPassCnf:
                    user.set_password(newPass)
                    user.save()
                    context['success'] = "Password Changed Successfully!"
                else:
                    context['error'] = "Password not matched!"
            else:
                context['error'] = "Wrong Password!"
    return render(request, 'dashboard/profile.html', context)
