#Manga.memorial

Django website to store virtual chapter bookmarks for manga, and notify the user of new manga chapters via email. Mangaupdates will be used for manga data.

#Build info
1. Use virtualenv and pip install using the requirements.txt
2. create a file called private_settings.py that looks like so:
```
p_settings = {
      'DJANGO_SECRET_KEY': 'randum',
      'PG_NAME': 'database_name',
      'PG_USER': 'username',
      'PG_PASS': 'correcthorsebatterystaple',
      'PG_HOST': 'localhost',
      'PG_PORT': '123456',
}
```
3. postgres must be installed, and the table and user entered above must be created 
4. python manage.py makemigrations
5. python manage.py migrate
6. python manage.py update_manga (takes a long time to complete)
7. python manage.py runserver
