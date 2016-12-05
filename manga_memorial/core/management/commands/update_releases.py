from django.core.management.base import BaseCommand, CommandError

from core.models import Manga
from lxml.html import parse

class Command(BaseCommand):
  help = 'Updates latest_release on mangas. Run every 12 hours at least.'

  def handle(self,*args, **options):
    url = 'http://www.mangaupdates.com/releases.html'
    root = parse(url).getroot()
    today_rls = root.xpath("//div/div[2]//tr[position()>=2]")

    for rls in today_rls:
      link = rls.xpath("./td[1]/a")
      Manga.objects.update_or_create(
        name=rls.xpath("./td[@class='pad']")[0].text_content(),
        defaults={
          'latest_release': rls.xpath("./td[2]")[0].text_content(),
          'manga_updates_url':link[0].get('href') if len(link) > 0 else None,
        },
      )
    

