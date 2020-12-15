from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


def signin_view(request):
    context = {
        'title': 'Sign In'
    }

    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/dashboard")
        else:
            context['login_error'] = "Invalid credentials!"
    return render(request, 'accounts/signin.html', context)


def signup_view(request):
    context = {
        'title': 'SignUp',
    }
    return render(request, 'accounts/signup.html', context)
