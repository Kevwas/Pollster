from django.shortcuts import render, redirect
from .forms import CreateUserForm, UserProfileForm
from .decorators import unauthenticated_user
from django.contrib.auth.models import User

from django.urls import reverse

from django.contrib import messages

from django.contrib.auth import authenticate, login, logout

# Create your views here.
@unauthenticated_user
def registerView(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()

            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            return redirect(reverse('accounts:login'))
    else:
        form = CreateUserForm()
        profile_form = UserProfileForm()

    context = {'form': form, 'profile_form': profile_form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('polls:polls', args=(1,)))
        else:
            messages.error(request, 'Incorrect Credentials')
    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):    
    logout(request)
    return redirect(reverse('accounts:login'))