from django.contrib import admin
from .models import User
from .models import Manga
from .models import Bookmark

# Register your models here.
admin.site.register(User)
admin.site.register(Manga)
admin.site.register(Bookmark)