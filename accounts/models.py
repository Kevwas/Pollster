from django.db import models
from django.contrib.auth.models import User
import json

from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(models.Model):
    #required by the auth model
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    polls_made = models.TextField(default='[]')
    polls_created = models.TextField(default='[]')
    identification = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, default='')
    followers = models.IntegerField(null=True, blank=True)
    following = models.IntegerField(null=True, blank=True)
    stars = models.IntegerField(null=True, blank=True)

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
