from django.db import models
from django.contrib.auth.models import User
import json


class UserProfile(models.Model):
    #required by the auth model
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    polls_made = models.TextField(default='[]')
    identification = models.IntegerField(null=True, blank=True)
    # age = models.IntegerField(null=True, blank=True)
    # location = models.CharField(max_length=50, null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, default='')

    def set_polls_made(self, poll):
        loaded_polls = self.get_polls_made()
        new_poll = int(poll)
        loaded_polls.append(new_poll)
        self.polls_made = json.dumps(loaded_polls)

    def get_polls_made(self):
        return json.loads(self.polls_made)
    get_polls_made.admin_order_field = 'polls_made'
    get_polls_made.short_description = 'Polls made.'

    def __str__(self):
        return self.user.username
