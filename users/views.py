from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from .forms import SignupForm, LoginForm


def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password == confirm_password:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username is already taken')
                    return redirect(register)
                else:
                    user = User.objects.create_user(
                        username=username, password=password)
                    user.save()
                    return redirect('login')

            else:
                messages.info(request, 'Both passwords are not matching')
                return redirect(register)

    else:
        return render(request, 'registration.html')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Invalid Username or Password')
                return redirect('login')

    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('home')
