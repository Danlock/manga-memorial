from django.conf.urls import url
from django.contrib.auth.views import login
from . import views
from core.views import *

urlpatterns = [
  url(r'^$', login),
  url(r'^logout/$', logout_page),
  url(r'^login/$', login), # If user is not login it will redirect to login page
  url(r'^register/$', register),
  url(r'^register/success/$', register_success),
  url(r'^home/$', home),
]