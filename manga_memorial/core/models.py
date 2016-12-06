import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Manga(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(max_length=2048,null=True)
  #newline seperated list of alternative names
  related_names = models.TextField(null=True)
  latest_release = models.CharField(max_length=128,null=True)
  author = models.CharField(max_length=128,default="",null=True)
  relevant_image_url = models.URLField(max_length=512,null=True)
  manga_updates_url = models.URLField(max_length=512,null=True)
  updated_at = models.DateTimeField(auto_now=True,null=True)

  def get_related_list(self):
    names = []
    if self['related_names'] != None:
      names = self['related_names'].split('\n')

    return names

class User(AbstractUser):
  frequency_choices = (
    ('never','never'),
    ('daily','daily'),
    ('bidaily','bidaily'),
    ('weekly','weekly'),
    ('biweekly','biweekly'),
    ('monthly','monthly'),
    ('bimonthly','bimonthly'),
  )
  private = models.BooleanField(default=True)
  notification_frequency = models.CharField(max_length=32,choices=frequency_choices,default=frequency_choices[0])
  created_at = models.DateTimeField(auto_now_add=True,null=True)
  updated_at = models.DateTimeField(auto_now=True,null=True)

class Bookmark(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  title = models.CharField(max_length=64, null=True)
  user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
  manga = models.ForeignKey(Manga,on_delete=models.SET_NULL,null=True)
  release = models.CharField(max_length=128,null=True)
  updated_at = models.DateTimeField(auto_now=True,null=True)
