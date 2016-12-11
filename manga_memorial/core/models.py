import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

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
    ('daily','daily'),
    ('bidaily','bidaily'),
    ('weekly','weekly'),
    ('biweekly','biweekly'),
    ('monthly','monthly'),
    ('bimonthly','bimonthly'),
  )
  frequency_choices_hours = {
    'never': -1,
    'daily':  24,
    'bidaily':  48,
    'weekly': 24*7,
    'biweekly': 24*14,
    'monthly':  24*30,
    'bimonthly':  24*60,
  }
  private = models.BooleanField(default=True)
  notification_frequency = models.CharField(max_length=32,choices=frequency_choices,default=frequency_choices[0][0])
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

class MangaList():
  manga_list = []

  @classmethod
  def getMangaList(self):
    return self.manga_list

  @classmethod
  def updateMangaList(self):
    sorted_mangas = [item for sm in Manga.objects.all() for item in sm.get_related_list()]
    sorted_mangas.sort()
    self.manga_list = sorted_mangas

  @classmethod
  def getMangaListForAutocomplete(self):
    try:
      self.updateMangaList()
    except Exception:
      print("WARNING: Failed to update manga list!")
    return [ (m,m) for m in self.manga_list ]


# MangaList.updateMangaList()