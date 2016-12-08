import time
from django.core.management.base import BaseCommand, CommandError
from core.models import Manga,MangaList
from lxml.html import parse
from lxml.cssselect import CSSSelector


MAX_MANGA_ID = 999999
CONSECUTIVE_ERROR_TOLERANCE = 25
selectors = dict(
  name=CSSSelector('.releasestitle'),
  release=CSSSelector('div.sContainer:nth-child(3) > div:nth-child(1) > div:nth-child(17)'),
  author=CSSSelector('div.sContainer:nth-child(4) > div:nth-child(1) > div:nth-child(17) > a:nth-child(1) > u:nth-child(1)'),
  image=CSSSelector('div.sContainer:nth-child(4) > div:nth-child(1) > div:nth-child(2) > center:nth-child(1) > img:nth-child(1)'),          
  related=CSSSelector('div.sContainer:nth-child(3) > div:nth-child(1) > div:nth-child(11)'),
  err=CSSSelector('.tab_middle'),
  err_body=CSSSelector('.table_content'),
)


class Command(BaseCommand):
  help = 'Grabs all manga titles and names from Bakaupdates. Expensive.'

  def handle(self,*args, **options):
    start_time = time.time()
    base_url = 'http://www.mangaupdates.com/series.html?id='

    consecutive_errors = 0
    index = 15000

    while (index < MAX_MANGA_ID):
      if (consecutive_errors >= CONSECUTIVE_ERROR_TOLERANCE):
        print('Error Tolerance Reached!')
        break

      url = base_url + str(index)
      
      try:
        root = parse(url).getroot()
      except Exception:
        print('Parse failed on ',url,'. Check your internet connection.')
        break;

      #If we have reached the an error page skip it
      err_elem = selectors['err'](root)
      err_body_elem = selectors['err_body'](root)
      if (len(err_elem) > 0):
        #Dont bother reporting errors about invalid ids
        if (err_body_elem[0].text_content().strip() != 'You specified an invalid series id.'):
          print('Failed on ',url)
          print(err_elem[0].text_content()  if len(err_elem) > 0 else " ")
          print(err_body_elem[0].text_content()  if len(err_body_elem) > 0 else " ")
        consecutive_errors += 1
        index += 1
        continue

      #if this page has a name, add to db
      nameElem = selectors['name'](root)
      if (len(nameElem) > 0):
        consecutive_errors = 0

        author_elem = selectors['author'](root)
        release_elem = selectors['release'](root)
        related_elem = selectors['related'](root)
        relevant_image_url_elem = selectors['image'](root)

        author = author_elem[0].text_content().strip() if len(author_elem) > 0 else None
        image_url = relevant_image_url_elem[0].get('src') if len(relevant_image_url_elem) > 0 else None
        release = release_elem[0].text_content().split('by')[0].strip() if len(release_elem) > 0 else None
        related = '\n'.join(related_elem[0].text_content().split('\n')[:-1]) if len(related_elem) > 0 else None


        Manga.objects.update_or_create(
          name=nameElem[0].text_content().strip(),
          defaults={
            'author': author,
            'manga_updates_url': url,
            'latest_release': release,
            'related_names': related,
            'relevant_image_url': image_url,
          }  
        )
      index += 1

    print('This took {0} seconds to run.'.format(time.time() - start_time))
    MangaList.updateMangaList()
