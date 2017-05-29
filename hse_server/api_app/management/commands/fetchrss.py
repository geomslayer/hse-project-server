from django.core.management.base import BaseCommand
from gensim.models.keyedvectors import KeyedVectors
from itertools import groupby
from pymorphy2 import MorphAnalyzer
from random import choice
from ...models import Category, News, Question
from ...settings import RSS_URL
import feedparser
import os.path
import time

MIN_LEN = 3
QUESTIONS = 3
ATTEMPTS = 20
HIDDEN = '________'

# change for real names
BIN_FILES = ['news.bin']
MODEL_PATH = os.path.expanduser('~/models')


class Command(BaseCommand):
    help = 'Fetches rss and adds new news'

    def handle(self, *args, **options):
        data = feedparser.parse(RSS_URL)
        cnt = 0

        morph = MorphAnalyzer()
        word_vectors = [KeyedVectors.load_word2vec_format(
            os.path.join(MODEL_PATH, file), binary=True) for file in BIN_FILES]

        # saving each news
        for entry in data.entries:
            try:
                category = Category.objects.get(text=entry.category)
            except Category.DoesNotExist:
                continue

            try:
                # trying to find the news
                News.objects.get(link=entry.id)
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

            original, answer, questions = generate_question(news.text, word_vectors, morph)
            if questions is None:
                news.delete()
                continue

            for question in questions:
                q = Question(
                    news=news,
                    text=question,
                    is_ans=(answer.normal_form == question)
                )
                q.save()

            news.text = hide_answer(original, news.text)
            news.hidden = original
            news.save()

        message = ('Successfully added %d news' % cnt) if cnt != 0 else 'Nothing new'
        self.stdout.write(self.style.SUCCESS(message))


def divide(text):
    words = []
    for key, group in groupby(text, key=lambda ch: ch.isalpha()):
        words.append(''.join(group))
    return words


def hide_answer(answer, text):
    return ''.join(map(lambda word: HIDDEN if word == answer else word,
                       divide(text)))


def text_to_words(text):
    text = ''.join(map(lambda ch: ch if ch.isalpha() else ' ', text))
    return [word for word in text.split() if len(word) > MIN_LEN]


def to_word(pair):
    raw = pair[0]
    return raw.rpartition('::')[2].split('_')[0]


def generate_question(text, word_vectors, morph):
    words = text_to_words(text)
    words = [word for word in words if 'NOUN' in morph.parse(word)[0].tag]
    questions = original = answer = None
    attempts_outer = 0
    while attempts_outer < ATTEMPTS and questions is None:
        attempts_outer += 1
        original = choice(words)
        answer = morph.parse(original)[0]
        similar = []
        for wv in word_vectors:
            try:
                similar.extend(wv.most_similar(answer.normal_form + '_NOUN')[:5])
            except KeyError:
                continue
        similar = list(filter(lambda elem: elem[0].split('_')[1] == 'NOUN', similar))
        similar = list(map(to_word, similar))
        if len(similar) == 0:
            continue
        questions = {answer.normal_form}
        attempts = 0
        while attempts < ATTEMPTS and len(questions) < QUESTIONS:
            questions.add(choice(similar))
            attempts += 1
    return original, answer, questions
