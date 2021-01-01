import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question, Choice


def create_question_with_choices(question_text, days, choices=3):
    """
    Create a question with the given 'question_text' and published the given
    number of 'days' offset to now (negative for questions published in the
    past, positive for questions that have yet to be published).
    And also with a given number of choices (default = 3) with it to make
    it valid.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    q = Question.objects.create(question_text=question_text, pub_date=time)
    for i in range(choices):
        Choice.objects.create(question=q, choice_text='Choice' + str(i))
    return q


def question_without_choices(obj, view_name):
    """
    The results of questions without choices are not displayed.
    """
    question = create_question_with_choices(question_text="Random Question.",
                                            days=0, choices=0)
    url = reverse('polls:' + view_name, args=(question.id,))
    response = obj.client.get(url)
    obj.assertEqual(response.status_code, 404)


def question_with_one_choice(obj, view_name):
    """
    The results of questions with only one choice are not displayed.
    """
    question = create_question_with_choices(question_text="Random Question.",
                                            days=0, choices=1)
    url = reverse('polls:' + view_name, args=(question.id,))
    response = obj.client.get(url)
    obj.assertEqual(response.status_code, 404)


def question_with_two_choices(obj, view_name):
    """
    The results of questions with two choices are displayed.
    """
    question = create_question_with_choices(question_text="Random Question.",
                                            days=0, choices=2)
    url = reverse('polls:' + view_name, args=(question.id,))
    response = obj.client.get(url)
    obj.assertContains(response, question.question_text)


def question_with_more_than_two_choices(obj, view_name):
    """
    The results of questions with more than two choices are displayed.
    """
    question = create_question_with_choices(question_text="Random Question.",
                                            days=0, choices=3)
    url = reverse('polls:' + view_name, args=(question.id,))
    response = obj.client.get(url)
    obj.assertContains(response, question.question_text)


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future returns a
        404 not found.
        """
        future_question = create_question_with_choices(
            question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question_with_choices(
            question_text='Future question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_question_without_choices(self):
        question_without_choices(self, 'detail')

    def test_question_with_one_choice(self):
        question_with_one_choice(self, 'detail')

    def test_question_with_two_choices(self):
        question_with_two_choices(self, 'detail')

    def test_question_with_more_than_two_choices(self):
        question_with_more_than_two_choices(self, 'detail')


class QuestionResultsViewTests(TestCase):
    def test_future_question(self):
        """
        The results view of a question with a pub_date in the future returns a
        404 not found.
        """
        future_question = create_question_with_choices(
            question_text='Future question.', days=5)
        url = reverse('polls:results', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The results view of a question with a pub_date in the past
        displays the vote's results.
        """
        past_question = create_question_with_choices(
            question_text='Past Question.', days=-5)
        url = reverse('polls:results', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_question_without_choices(self):
        question_without_choices(self, 'results')

    def test_question_with_one_choice(self):
        question_with_one_choice(self, 'results')

    def test_question_with_two_choices(self):
        question_with_two_choices(self, 'results')

    def test_question_with_more_than_two_choices(self):
        question_with_more_than_two_choices(self, 'results')


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropiate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the index page.
        """
        create_question_with_choices(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: Past question.>'])

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on the index
        page.
        """
        create_question_with_choices(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_question_with_choices(question_text="Past question.", days=-30)
        create_question_with_choices(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question_with_choices(question_text="Past question 1.",
                                     days=-30)
        create_question_with_choices(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

    def test_question_without_choices(self):
        """
        The questions without choices are not displayed.
        """
        create_question_with_choices(question_text="Random Question.", days=0,
                                     choices=0)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_question_with_one_choice(self):
        """
        The questions with only one choice are not displayed.
        """
        create_question_with_choices(question_text="Random Question.", days=0,
                                     choices=1)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_question_with_two_choices(self):
        """
        The questions with two choices are displayed.
        """
        create_question_with_choices(
            question_text="Random Question.", days=0, choices=2)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Random Question.>']
        )

    def test_question_with_more_than_two_choices(self):
        """
        The questions with more than two choices are displayed.
        """
        create_question_with_choices(question_text="Random Question.",
                                     days=0, choices=3)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Random Question.>']
        )


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """ was_published_recently() returns False for questions whose
            pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """ was_published_recently() returns False for questions whose pub_date
            is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """ was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23,
                                                   minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)
