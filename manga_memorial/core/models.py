import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
'''
monkeypatch dealing with no UUID serialization support in default json
Credit goes to https://arthurpemberton.com/2015/04/fixing-uuid-is-not-json-serializable
TODO: get rid of once django update this bullshit
'''
from json import JSONEncoder
from uuid import UUID
JSONEncoder_olddefault = JSONEncoder.default
def JSONEncoder_newdefault(self, o):
    if isinstance(o, UUID): return str(o)
    return JSONEncoder_olddefault(self, o)
JSONEncoder.default = JSONEncoder_newdefault


# Create your models here.
class Manga(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(max_length=4096,null=True)
  related_names = ArrayField(models.CharField(max_length=4096,null=True),default=list)
  latest_release = models.CharField(max_length=128,null=True)
  translator = models.CharField(max_length=256,default="",null=True)
  translator_url = models.URLField(max_length=512,null=True)
  author = models.CharField(max_length=128,default="",null=True)
  relevant_image_url = models.URLField(max_length=512,null=True)
  manga_updates_url = models.URLField(max_length=512,null=True)
  updated_at = models.DateTimeField(auto_now=True,null=True)

  def get_related_list(self):
    names = []
    if len(self.related_names) > 0:
      names.extend(self.related_names)
    names.append(self.name)
    return names

class User(AbstractUser):
  frequency_choices = (
    ('never','never'),
    ('noonly','noonly'),
    ('daily','daily'),
    ('bidaily','bidaily'),
    ('weekly','weekly'),
    ('biweekly','biweekly'),
    ('monthly','monthly'),
    ('bimonthly','bimonthly'),
  )
  frequency_choices_hours = {
    'never': -1,
    'noonly': 12,
    'daily':  24,
    'bidaily':  48,
    'weekly': 24*7,
    'biweekly': 24*14,
    'monthly':  24*30,
    'bimonthly':  24*60,
  }
  private = models.BooleanField(default=True)
  notification_frequency = models.CharField(max_length=32,choices=frequency_choices,default=frequency_choices[2][0])
  emailed_at =models.DateTimeField(null=True)
  created_at = models.DateTimeField(auto_now_add=True,null=True)
  updated_at = models.DateTimeField(auto_now=True,null=True)

class Bookmark(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  title = models.CharField(max_length=64, null=True)
  user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
  manga = models.ForeignKey(Manga,on_delete=models.SET_NULL,null=True)
  release = models.CharField(max_length=128,null=True)
  updated_at = models.DateTimeField(auto_now=True,null=True)
