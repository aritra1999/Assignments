from django.shortcuts import render


def signin_view(request):
    context = {
        'title': 'SignIn',
    }
    return render(request, 'accounts/signin.html', context)


def signup_view(request):
    context = {
        'title': 'SignUp',
    }
    return render(request, 'accounts/signup.html', context)
