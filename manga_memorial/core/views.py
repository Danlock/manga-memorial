from django.shortcuts import render
from django.http import HttpResponse
from core.forms import *
from core import models
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

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
      return HttpResponseRedirect('/register/success/')
  else:
    form = RegistrationForm()
  
  variables = RequestContext(request, {
    'form': form
  })
  return render_to_response(
    'registration/register.html',
    variables,
  )

def register_success(request):
  return render_to_response(
    'registration/success.html',
  )

def logout_page(request):
  logout(request)
  return HttpResponseRedirect('/')


@login_required
@csrf_protect
def home(request):
  if request.method == 'POST':
    form = BookmarkForm(request.POST)
    if form.is_valid():
      bm = models.Bookmark(
        manga=models.Manga.objects.get(name=form.cleaned_data['manga']),
        release=form.cleaned_data['release'],
        user=request.user,
      )
      if ('title' in form.cleaned_data):
        bm.title = form.cleaned_data['title']
      bm.save()

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
def delete_bookmark(request):
  if request.method == "DELETE":
    print(request.POST)
