import feedparser
import time
from models import *

URL = 'https://lenta.ru/rss'

data = feedparser.parse(URL)

file_prev = open('last-rss.txt', 'r')
str_prev = file_prev.readline().strip()
file_prev.close()

str_new = data.entries[0].id

# nothing new
if str_prev == str_new:
    exit(0)

# saving identificator of rss page
file_new = open('last-rss.txt', 'w')
print(str_new, file=file_new)
file_new.close()

# connecting to db
connect(DB_NAME)
init_category()

# saving each news
for entry in data.entries:
    cats = Category.objects(text=entry.category)

    if len(cats) == 0:
        category = Category(text=entry.category)
        continue

    category = cats[0]

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
