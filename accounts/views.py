from django.shortcuts import render, redirect
from .forms import CreateUserForm, UserProfileForm, UserProfileExtraInfoForm, UserForm
from .decorators import unauthenticated_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.urls import reverse

from django.contrib import messages

from django.contrib.auth import authenticate, login, logout

# Create your views here.
@unauthenticated_user
def registerView(request):
    # print(request)
    # Clear all messages
    system_messages = messages.get_messages(request)
    for message in system_messages:
        # This iteration is necessary
        pass
    # Messages cleared.
    if request.method == 'POST':
        print("POST")
        form = CreateUserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            # A django signal creates the user profiles after creating an user
            user.userprofile.identification = profile_form.cleaned_data.get('identification')
            user.userprofile.phone = profile_form.cleaned_data.get('phone')
            user.userprofile.location = profile_form.cleaned_data.get('location')
            user.userprofile.save()

            username = form.cleaned_data.get('username')

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


def logoutUser(request):    
    print(request)
    logout(request)
    return redirect(reverse('accounts:login'))

@login_required
def ProfileView(request, username):
    user_profile = request.user.userprofile
    user_profile_form = UserProfileExtraInfoForm(instance=user_profile)
    user_form = UserForm(instance=request.user)
    polls_made = user_profile.get_polls_made()
    polls_created = user_profile.get_polls_created()

    if request.method == "POST":
        # print("REQUEST IS A POST!")
        user_profile_form = UserProfileExtraInfoForm(request.POST, request.FILES, instance=user_profile)
        user_form = UserForm(request.POST, instance=request.user)
        # print(request.FILES)
        # print(request.POST)

        # Clear all messages
        system_messages = messages.get_messages(request)
        for message in system_messages:
            # This iteration is necessary
            pass
        # Messages cleared.

        if user_profile_form.is_valid() and user_form.is_valid():
            # print("FORM IS VALID!")
            user_profile_form.save()
            user_form.save()
            messages.success(request, 'User info updated')
        else:
            # print("FORM IS NOT VALID!")
            messages.error(request, {
                'user_profile_form': user_profile_form,
                'user_form': user_form,
            })

    context = {'user_profile_form': user_profile_form, 'uer_form': user_form,
                'polls_made': polls_made, 'polls_created': polls_created}

    return render(request, 'accounts/profile.html', context)