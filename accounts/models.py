from django.db import models
from django.contrib.auth.models import User
import json
from phonenumber_field.modelfields import PhoneNumberField
# from django.contrib.auth.models import AbstractUser


class UserProfile(models.Model):
    # required by the auth model
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    polls_made = models.TextField(default='[]')
    polls_created = models.TextField(default='[]')
    identification = models.TextField(max_length=200, null=True, blank=True, unique=True)
    location = models.TextField(max_length=200, null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, default='user_default.png')
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)
    stars = models.IntegerField(default=0)
    bio = models.TextField(max_length=500, null=True, blank=True, default='Bio')
    

    def set_polls_made(self, poll):
        loaded_polls = self.get_polls_made()
        new_poll = int(poll)
        loaded_polls.append(new_poll)
        self.polls_made = json.dumps(loaded_polls)

    def get_polls_made(self):
        return json.loads(self.polls_made)
    get_polls_made.admin_order_field = 'polls_made'
    get_polls_made.short_description = 'Polls made.'

    def set_polls_created(self, poll):
        loaded_polls = self.get_polls_created()
        new_poll = int(poll)
        loaded_polls.append(new_poll)
        self.polls_created = json.dumps(loaded_polls)

    def get_polls_created(self):
        return json.loads(self.polls_created)
    get_polls_created.admin_order_field = 'polls_created'
    get_polls_created.short_description = 'Polls created.'


    def __str__(self):
        return str(self.user)


# class User(AbstractUser):
#     profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, blank=True)

#     class Meta:
#         abstract = True
