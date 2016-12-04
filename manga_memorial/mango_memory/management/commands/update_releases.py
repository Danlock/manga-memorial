from django.core.management.base import BaseCommand, CommandError

from mango_memory.models import Manga
from lxml.html import parse

class Command(BaseCommand):
  help = 'Updates latest_release on manga.'

  # def add_arguments(self, parser):
  #     # Positional arguments
  #     parser.add_argument('poll_id', nargs='+', type=int)

  #     # Named (optional) arguments
  #     parser.add_argument('--delete',
  #         action='store_true',
  #         dest='delete',
  #         default=False,
  #         help='Delete poll instead of closing it')

  def handle(self,*args, **options):
    url = 'http://www.mangaupdates.com/releases.html'
    root = parse(url).getroot()
    today_rls = root.xpath("//div/div[2]//tr[position()>=2]")


    for rls in today_rls:
      link = rls.xpath("./td[1]/a")
      Manga.objects.get_or_create(
        name=rls.xpath("./td[@class='pad']")[0].text_content(),
        defaults={
          'latest_release': rls.xpath("./td[2]")[0].text_content(),
          'manga_updates_url':link[0].get('href') if len(link) > 0 else None,
        },
      )
    

