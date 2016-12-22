from .models import User,Bookmark
from django.db.models import Q
from django.core.mail import get_connection,EmailMessage,EmailMultiAlternatives
from datetime import datetime,timedelta,timezone
from django.template.loader import render_to_string

def getAndUpdateBookmarks(user): 
  bookmarks = []
  for bm in Bookmark.objects.filter(user=user):
    #this line is in case a bookmark has no release at all, leftover from old design
    bm.release = bm.manga.latest_release if not bm.release else bm.release 
    if (bm.manga.latest_release != bm.release):
      bookmarks.append(bm)
    bm.release = bm.manga.latest_release
    bm.save()
  return bookmarks

def shouldEmail(user):
  hours = User.frequency_choices_hours[user.notification_frequency]
  relevantTime = user.created_at if user.emailed_at == None else user.emailed_at
  if (hours == -1 or user.email == None):
    return False
  elif (relevantTime + timedelta(hours=hours) < datetime.now(timezone.utc)):
    return True
  else:
    return False

def notifyAllUsers():
  users = User.objects.exclude(Q(email__isnull=True) | Q(notification_frequency=User.frequency_choices[0][0]))
  conn = get_connection()
  emails = []
  for user in users:
    if (shouldEmail(user)):
      bookmarks = getAndUpdateBookmarks(user)
      if (len(bookmarks) > 0):
        email = EmailMultiAlternatives(
          'Your manga.memorial release notifications!',
          render_to_string('email.txt', {'bookmarks': bookmarks}),
          'dan@manga.memorial',
          [user.email],
        )
        email.attach_alternative(render_to_string('email.html', {'bookmarks': bookmarks}),"text/html")
        emails.append(email)
        user.emailed_at = datetime.now(timezone.utc)
        user.save()

  if (len(emails) > 0):
    conn.send_messages(emails)
  return
