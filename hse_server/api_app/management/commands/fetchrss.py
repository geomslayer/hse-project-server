from django.core.management.base import BaseCommand, CommandError
from api_app.models import Category, News
from api_app.settings import RSS_URL
import feedparser
import time


class Command(BaseCommand):
    help = 'Fetches rss and adds new news'

    def handle(self, *args, **options):
        data = feedparser.parse(RSS_URL)
        cnt = 0

        # saving each news
        for entry in data.entries:
            try:
                category = Category.objects.get(text=entry.category)
            except Category.DoesNotExist:
                continue

            try:
                news = News.objects.get(link=entry.id)
                continue
            except News.DoesNotExist:
                pass

            news = News()
            news.category = category
            news.title = entry.title
            news.text = entry.summary

            # time in milliseconds
            news.date = int(time.mktime(entry.published_parsed) * 1000)
            news.link = entry.id

            if len(entry.enclosures) > 0:
                news.img = entry.enclosures[0]['href']

            news.save()
            cnt += 1

        message = ('Successfully added %d news' % cnt) if cnt != 0 else 'Nothing new'
        self.stdout.write(self.style.SUCCESS(message))
