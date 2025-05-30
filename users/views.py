"""
User authentication views.

This module contains view functions for user registration, login, and logout.
"""

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .forms import SignupForm, LoginForm
import logging

logger = logging.getLogger(__name__)


def register(request):
    """
    User registration view.
    Handles both GET (display form) and POST (process registration).
    """
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect('home')
    
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                
                # Create new user
                user = User.objects.create_user(
                    username=username,
                    password=password
                )
                user.save()
                
                messages.success(request, f'Account created successfully for {username}! You can now log in.')
                logger.info(f'New user registered: {username}')
                return redirect('login')
                
            except Exception as e:
                logger.error(f'Error creating user: {str(e)}')
                messages.error(request, 'An error occurred while creating your account. Please try again.')
        
        else:
            # Form validation failed
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.title()}: {error}')
    
    else:
        form = SignupForm()
    
    context = {
        'form': form,
        'title': 'Create Account'
    }
    return render(request, 'registration.html', context)


def login(request):
    """
    User login view.
    Handles both GET (display form) and POST (process login).
    """
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Authenticate user
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    messages.success(request, f'Welcome back, {username}!')
                    logger.info(f'User logged in: {username}')
                    
                    # Redirect to next page or home
                    next_page = request.GET.get('next')
                    return redirect(next_page if next_page else 'home')
                else:
                    messages.error(request, 'Your account is disabled.')
            else:
                messages.error(request, 'Invalid username or password.')
                logger.warning(f'Failed login attempt for username: {username}')
        
        else:
            # Form validation failed
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.title()}: {error}')
    
    else:
        form = LoginForm()
    
    context = {
        'form': form,
        'title': 'Login'
    }
    return render(request, 'login.html', context)


def logout(request):
    """
    User logout view.
    Logs out the current user and redirects to login page.
    """
    if request.user.is_authenticated:
        username = request.user.username
        auth_logout(request)
        messages.success(request, f'You have been logged out successfully, {username}.')
        logger.info(f'User logged out: {username}')
    else:
        messages.info(request, 'You were not logged in.')
    
    return redirect('login')
