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

def index(request):
    return render(request, 'pages/index.html')

def resultsData(request, obj):
    voteData = []

    question = Question.objects.get(id=obj)
    choices = question.choice_set.all()

    for choice in choices:
        voteData.append({choice.choice_text: choice.votes})

    print(voteData)
    return JsonResponse(voteData, safe=False)

ITEMS_PER_PAGE = 2
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
        )


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
    if question_id in polls_made:
        # Redirect to the polls
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You have already done this poll.",
        })
    else:
        try:
            select_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
        else:
            select_choice.votes = F('votes') + 1
            select_choice.save()
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
    ordering = ['-pub_date']
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
        )

        questions_to_return = []
        for question in questions:
            # print(question.id)
            if question.id in polls_made:
                # print("MATCH!")
                questions_to_return.append(question)

        return questions_to_return

# Index
# 1
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return HttpResponse(template.render(context, request))

# 2
# A shorcut: render()
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return render(request, 'polls/index.html', context)

# Detail
# 1
# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)

# Long version for raising a 404
# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, 'polls/detail.html', {'question': question})

# 2
# A shortcut: get_object_or_404()
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})

# Results
# 1
# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)

# 2
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})
