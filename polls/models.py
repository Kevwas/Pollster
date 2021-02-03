import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class Question(models.Model):
    creator = models.OneToOneField(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    description_text = models.TextField('brief description')
    multiple_choice = models.BooleanField(default=0)

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def multiple_choice_selection(self):
        return bool(self.multiple_choice)
    
#commit
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    choice_text = models.CharField(max_length=150)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
