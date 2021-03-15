from django import forms
from django.forms import ModelForm
# from django.contrib.auth.models import User
from django.db import models
from .models import Question, Choice
# from django.core.exceptions import ValidationError

class CreateQuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ('question_text', 'description_text', 'multiple_choice',)
        

class CreateChoiceForm(ModelForm):
    class Meta:
        model = Choice
        fields = ('choice_text',)

