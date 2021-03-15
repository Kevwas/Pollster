from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse  # Http404
from django.urls import reverse
from django.db.models import F, Q, Count
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.template import loader
from .models import Question, Choice
from django.contrib.auth.models import User
import json
from django.contrib import messages
# from .forms import CreateChoiceForm, CreateQuestionForm
import datetime
from .forms import CreateQuestionForm, CreateChoiceForm

def index(request):
    return render(request, 'pages/index.html')

def resultsData(request, obj):
    voteData = []

    question = Question.objects.get(id=obj) 
    choices = question.choice_set.all()

    for choice in choices:
        voteData.append({choice.choice_text: choice.votes})

    # print(voteData)
    return JsonResponse(voteData, safe=False)

ITEMS_PER_PAGE = 10
# 3 Generic views:
# class PollsView(LoginRequiredMixin, generic.ListView):
class PollsView(generic.ListView):
    # login_url = 'accounts:login'
    # redirect_field_name = 'redirect_to'
    template_name = 'polls/polls.html'
    context_object_name = 'latest_question_list'
    ordering = ['-pub_date']
    paginate_by = ITEMS_PER_PAGE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            user_profile = self.request.user.userprofile
            polls_made = json.loads(user_profile.polls_made)
            context['polls_made'] = polls_made
            
        return context

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet
        and those with less than 2 choices.
        """
        return Question.objects.exclude(
            choice__isnull=True).annotate(Count('choice')).exclude(
            choice__count__lte=1).filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')


class DetailView(LoginRequiredMixin, generic.DetailView):
    login_url = 'accounts:login'
    redirect_field_name = 'redirect_to'

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet
        and those with less than 2 choices.
        """
        return Question.objects.exclude(
            choice__isnull=True).annotate(Count('choice')).exclude(
            choice__count__lte=1).filter(pub_date__lte=timezone.now())


# class ResultsView(LoginRequiredMixin, generic.DetailView):
class ResultsView(generic.DetailView):
    # login_url = 'accounts:login'
    # redirect_field_name = 'redirect_to'

    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet
        and those with less than 2 choices.
        """
        return Question.objects.exclude(
            choice__isnull=True).annotate(Count('choice')).exclude(
            choice__count__lte=1).filter(pub_date__lte=timezone.now())

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    user_profile = request.user.userprofile
    polls_made = user_profile.get_polls_made()
    if question.id in polls_made:
        # Redirect to the polls
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You have already done this poll.",
        })
    else:
        try:
            choices = []
            # print(request.POST.getlist('choice'))
            for choice in request.POST.getlist('choice'):
                # print("Choice: " + choice)
                choices.append(question.choice_set.get(pk=choice))
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
        else:
            for choice in choices:
                choice.votes = F('votes') + 1
                choice.save()
            user_profile.set_polls_made(question.id)
            user_profile.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back Button.
            messages.success(request, 'You have voted on ' + question.question_text)
            return HttpResponseRedirect(reverse('polls:results',
                                        args=(question.id,)))

class DashboardView(LoginRequiredMixin, generic.ListView):
    login_url = 'accounts:login'
    redirect_field_name = 'redirect_to'
    template_name = 'pages/dashboard.html'
    context_object_name = 'latest_question_list'
    # ordering = ['-pub_date']
    paginate_by = ITEMS_PER_PAGE

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet
        and those with less than 2 choices.
        """
        user_profile = self.request.user.userprofile
        polls_made = json.loads(user_profile.polls_made)

        questions = Question.objects.exclude(
            choice__isnull=True).annotate(Count('choice')).exclude(
            choice__count__lte=1).filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')

        questions_to_return = []
        for question in questions:
            # print(question.id)
            if question.id in polls_made:
                # print("MATCH!")
                questions_to_return.append(question)

        return questions_to_return

@login_required
def CreatePollView(request):
    question_form = CreateQuestionForm()
    choice_form = CreateChoiceForm()
    user_profile = request.user.userprofile

    if request.method == "POST":
        question_form = CreateQuestionForm(request.POST)
        choice_form = CreateChoiceForm(request.POST)
        
        # Clear all messages
        system_messages = messages.get_messages(request)
        for message in system_messages:
            # This iteration is necessary
            pass
        # Messages cleared.
        if question_form.is_valid() and choice_form.is_valid():
            # print("FORM IS VALID!")
            question = Question(question_text=question_form.cleaned_data.get('question_text'), 
                                description_text=question_form.cleaned_data.get('description_text'), 
                                multiple_choice=question_form.cleaned_data.get('multiple_choice'),
                                creator=request.user)
            question.save()
            for choice in request.POST.getlist('choice'):
                # print("Choice: " + choice)
                ch = Choice(choice_text=choice, creator=request.user, question=question)
                ch.save()
            user_profile.set_polls_created(question.id)
            messages.success(request, 'Poll created succesfully!')
        else:
            # print("FORM IS NOT VALID!")
            messages.error(request, {
                'question_form': question_form,
                'choice_form': choice_form,
            })

    context = {'question_form': question_form, 'choice_form': choice_form}

    return render(request, 'polls/create_poll.html', context)


# @login_required
# def AddChoicesView(request):
#     user_profile = request.user.userprofile
#     user_profile_form = UserProfileExtraInfoForm(instance=user_profile)
#     user_form = UserForm(instance=request.user)
#     polls_made = user_profile.get_polls_made()
#     polls_created = user_profile.get_polls_created()

#     if request.method == "POST":
#         # print("REQUEST IS A POST!")
#         user_profile_form = UserProfileExtraInfoForm(request.POST, request.FILES, instance=user_profile)
#         user_form = UserForm(request.POST, instance=request.user)
#         # print(request.FILES)
#         # print(request.POST)

#         # Clear all messages
#         system_messages = messages.get_messages(request)
#         for message in system_messages:
#             # This iteration is necessary
#             pass
#         # Messages cleared.

#         if user_profile_form.is_valid() and user_form.is_valid():
#             # print("FORM IS VALID!")
#             user_profile_form.save()
#             user_form.save()
#             messages.success(request, 'User info updated')
#         else:
#             # print("FORM IS NOT VALID!")
#             messages.error(request, {
#                 'user_profile_form': user_profile_form,
#                 'user_form': user_form,
#             })

#     context = {'user_profile_form': user_profile_form, 'uer_form': user_form,
#                 'polls_made': polls_made, 'polls_created': polls_created}

#     return render(request, 'accounts/profile.html', context)
