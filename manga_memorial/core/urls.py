from django.conf.urls import url
from django.contrib.auth.views import login
from . import views
from core.views import *

urlpatterns = [
  url(r'^$', home),
  url(r'^logout/$', logout_page),
  url(r'^login/$', login), # If user is not login it will redirect to login page
  url(r'^register/$', register),
  url(r'^home/$', home),
  url(r'^bookmark/$', edit_bookmark),
]