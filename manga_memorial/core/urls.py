from django.conf.urls import url
from django.contrib.auth.views import login,password_change,password_change_done,password_reset,password_reset_done,password_reset_confirm,password_reset_complete
from . import views
from core.views import *

urlpatterns = [
  url(r'^$', home),
  url(r'^logout/$', logout_page),
  url(r'^login/$', login), # If user is not login it will redirect to login page
  url(r'^register/$', register),
  url(r'^profile/$', profile),
  url(r'^home/$', home),
  url(r'^manga/list/$', getMangaList),
  url(r'^bookmark/$', edit_bookmark),
  url(r'^password_change/$', password_change),
  url(r'^password_change/done/$', password_change_done,name="password_change_done"),
  # url(r'^password_reset/$', password_reset),
  # url(r'^password_reset/done/$', password_reset_done),
  # url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', password_reset_confirm),
  # url(r'^reset/done/$', password_reset_complete),
]