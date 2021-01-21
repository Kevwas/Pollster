from django.shortcuts import render, redirect
from .forms import CreateUserForm, UserProfileForm
from .decorators import unauthenticated_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.urls import reverse

from django.contrib import messages

from django.contrib.auth import authenticate, login, logout

# Create your views here.
@unauthenticated_user
def registerView(request):
    print(request)
    if request.method == 'POST':
        print("POST")
        form = CreateUserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            # user = form.save()
            
            # profile = profile_form.save(commit=False)
            # profile.user = user

            # profile.save()

            profile = profile_form.save()
            
            user = form.save(commit=False)
            user.profile = profile

            user.save()

            username = form.cleaned_data.get('username')
            # Clear all messages
            system_messages = messages.get_messages(request)
            for message in system_messages:
                # This iteration is necessary
                pass
            # Messages cleared.

            # Send success message
            messages.success(request, 'Account was created for ' + username)
            return redirect(reverse('accounts:login'))
        else:
            messages.error(request, {
                'form': form,
                'profile_form': profile_form,
            })
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

@login_required
def ProfileView(request, username):
    context = {}
    return render(request, 'accounts/profile.html', context)

def logoutUser(request):    
    logout(request)
    return redirect(reverse('accounts:login'))