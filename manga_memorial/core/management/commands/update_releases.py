from django.core.management.base import BaseCommand, CommandError

from core.models import Manga
from core.emails import notifyAllUsers
from lxml.html import parse

class Command(BaseCommand):
  help = 'Updates latest_release on mangas. Run every 6 hours at least.'

  def handle(self,*args, **options):
    url = 'http://www.mangaupdates.com/releases.html'
    root = parse(url).getroot()
    today_rls = root.xpath("//div/div[2]//tr[position()>=2]")

    for rls in today_rls:
      link = rls.xpath("./td[1]/a")
      group = rls.xpath("./td//a[@title='Group Info']")[0]
      group_name = group.text_content()
      group_url = group.get('href')

      name = rls.xpath("./td[@class='pad']")[0].text_content()
      name = name[:-1] if name[-1:] == "*" else name
      print("Updating ",name)
      Manga.objects.update_or_create(
        name=name,
        defaults={
          'latest_release': rls.xpath("./td[2]")[0].text_content(),
          'manga_updates_url': link[0].get('href') if len(link) > 0 else None,
          'translator': group_name,
          'translator_url': group_url,
        },
      )
    
    notifyAllUsers()
