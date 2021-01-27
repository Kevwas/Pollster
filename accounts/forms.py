from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.db import models
from .models import UserProfile
from django.core.exceptions import ValidationError
# from django.utils.translation import gettext_lazy as _


MAX_UPLOAD_SIZE = "2621440"

# Form to use when registering a new user
class CreateUserForm(UserCreationForm, ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

# Form to use when registering for extra user info
class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('identification', 'phone', 'location',)

# Form to use when changing user profile info
class UserProfileExtraInfoForm(ModelForm):
    def clean(self):
        self.check_file()
        return self.cleaned_data

    def check_file(self):
        profile_pic = self.cleaned_data["profile_pic"]
        # content_type = profile_pic.content_type.split('/')[0]
        if profile_pic:
            # Only do something if the image field is valid.
            if profile_pic.size > int(MAX_UPLOAD_SIZE):
                raise ValidationError({"profile_pic":["The picture size is to big. The maximun size allowed is 2.5mb"]})


    class Meta:
        model = UserProfile
        fields = ('profile_pic', 'phone', 'location', 'identification', 'bio',)
        # fields = '__all__'b

# Form to use when changing user info
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)