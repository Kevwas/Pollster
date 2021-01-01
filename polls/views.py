from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect  # Http404
from django.urls import reverse
from django.db.models import F, Q, Count
from django.views import generic
from django.utils import timezone
# from django.template import loader

from .models import Question, Choice


def index(request):
  return render(request, 'pages/index.html')


# 3 Generic views:
class PollsView(generic.ListView):
    template_name = 'polls/polls.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions (not including
        those set to be
        published in the future).
        """
        return Question.objects.exclude(
            choice__isnull=True).annotate(Count('choice')).exclude(
            choice__count__lte=1).filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.exclude(
            choice__isnull=True).annotate(Count('choice')).exclude(
            choice__count__lte=1).filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.exclude(
            choice__isnull=True).annotate(Count('choice')).exclude(
            choice__count__lte=1).filter(pub_date__lte=timezone.now())


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
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
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back Button.
        return HttpResponseRedirect(reverse('polls:results',
                                    args=(question.id,)))

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
