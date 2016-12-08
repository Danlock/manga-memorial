from .models import User,Bookmark
from django.db.models import Q
from django.core.mail import get_connection,EmailMessage
from datetime import datetime,timedelta,timezone



def relevantBookmarks(user): 
  bookmarks = []
  for bm in Bookmark.objects.filter(user=user):
    if (bm.manga.latest_release != bm.release):
      bookmarks.append(bm)
  return bookmarks

def shouldEmail(user):
  hours = User.frequency_choices_hours[user.notification_frequency]
  if (hours == -1):
    return False
  elif (user.emailed_at == None or user.emailed_at + timedelta(hours=hours) < datetime.now(timezone.utc)):
    return True
  else:
    return False

def notifyAllUsers():
  users = User.objects.exclude(Q(email__isnull=True) | Q(notification_frequency=User.frequency_choices[0][0]))
  conn = get_connection()
  emails = []
  for user in users:
    if (shouldEmail(user)):
      bookmarks = relevantBookmarks(user)
      if (len(bookmarks) > 0):
        message = str(bookmarks)
        emails.append(EmailMessage(
          'Your {} manga release notifications!'.format(user.notification_frequency),
          message,
          'mangamemorialupdates@gmail.com',
          [user.email],
        ))
        user.emailed_at = datetime.now(timezone.utc)
        user.save()

  print('emails:',len(emails))
  if (len(emails) > 0):
    conn.send_messages(emails)
  return
