from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.utils import timezone

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404


def home(request):
    return render(request, 'accounts/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'accounts/sign_up_user.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'accounts/sign_up_user.html', {'form': UserCreationForm(),
                                                                  'error': 'Пользователь с подобным логином уже зарегистрирован в системе'})
        else:
            return render(request, 'accounts/sign_up_user.html', {'form': UserCreationForm(),
                                                              'error': 'Пароли не схожи между собой'})


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'accounts/login.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'accounts/sign_up_user.html',
                          {'form': UserCreationForm(), 'error': 'Не нашел такого пользователя или такого пароля'})
        else:
            login(request, user)
            cache.clear()
            return redirect('home')

