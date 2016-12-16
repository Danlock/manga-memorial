from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Q
from dal import autocomplete

from core.forms import *
from core import models

User = get_user_model()

@csrf_protect
def register(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      user = User.objects.create_user(
        password=form.cleaned_data['password1'],
        username=form.cleaned_data['username'],
        email=form.cleaned_data['email']
      )
      return HttpResponseRedirect('/home/')
  else:
    form = RegistrationForm()
  
  variables = RequestContext(request, {
    'form': form
  })
  return render_to_response(
    'registration/register.html',
    variables,
  )

def logout_page(request):
  logout(request)
  return HttpResponseRedirect('/')

@login_required
@csrf_protect
def profile(request):
  if request.method == 'POST':
    form = ProfileForm(request.POST)
    if form.is_valid():
      data = {
        'notification_frequency': form.cleaned_data['notifications'],
      }
      #if user updated their email, then save it
      if form.cleaned_data['email'] != None:
        data['email'] = form.cleaned_data['email']
      models.User.objects.filter(id=request.user.id).update(**data)
      return HttpResponseRedirect('/profile/')
  else:
    form = ProfileForm(initial={
      'email': request.user.email,
      'notifications':request.user.notification_frequency,
    })
  
  variables = RequestContext(request, {
    'form': form,
    'user': request.user,
  })

  return render_to_response(
    'profile.html',
    variables,
  )

@login_required
@csrf_protect
def home(request):
  if request.method == 'POST':
    form = BookmarkForm(request.POST)
    if form.is_valid():
      for manga in form.cleaned_data['multiple_manga']:
        models.Bookmark(
          manga=manga,
          release=manga.latest_release,
          user=request.user,
        ).save()

      return HttpResponseRedirect('/home/')
  else:
    form = BookmarkForm()
  
  variables = RequestContext(request, {
    'form': form,
    'user': request.user,
    'bookmarks': models.Bookmark.objects.filter(user__id=request.user.id),
  })

  return render_to_response(
    'home.html',
    variables,
  )

@login_required
@csrf_protect
def editBookmark(request):
  if request.method == "POST":
    models.Bookmark(pk=request.POST['pk'],release=request.POST['value']).save(update_fields=['release'])
  if request.method == "DELETE":
    print("delete return",request.body.decode('utf-8'))
    models.Bookmark(pk=request.body.decode('utf-8')).delete()

  return HttpResponse()

class MangaAutocomplete(autocomplete.Select2QuerySetView):
  def get_queryset(self):
    if not self.request.user.is_authenticated():
      return models.Manga.objects.none()

    qs = models.Manga.objects.all()

    if self.q:
      #need to query manga name and some of its related names
      query = (Q(name__icontains=self.q) 
        | Q(related_names__0__icontains=self.q) 
        | Q(related_names__1__icontains=self.q)  
        | Q(related_names__2__icontains=self.q)  
        | Q(related_names__3__icontains=self.q)  
        | Q(related_names__4__icontains=self.q)  
        | Q(related_names__5__icontains=self.q) 
        | Q(related_names__6__icontains=self.q))
      qs = qs.filter(query)

    return qs 

  def get_result_value(self, result):
    return result.id

  def get_result_label(self, result):
    return result.name