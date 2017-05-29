from django.http import HttpResponse
from django.db.models import Q
from rest_framework.renderers import JSONRenderer
from .models import Category, News, Question
from .serializers import CategorySerializer, NewsSerializer, QuestionSerializer
from .settings import LIMIT


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def get_categories(request):
    cats = Category.objects.all()
    serializer = CategorySerializer(cats, many=True)
    return JSONResponse(serializer.data)


def get_category(request, pk):
    cat = Category.objects.get(pk=pk)
    serializer = CategorySerializer(cat)
    return JSONResponse(serializer.data)


def get_news(request, category_id):
    news_list = News.objects.order_by('-date', '-id').filter(category_id=category_id)[:LIMIT]
    serializer = NewsSerializer(news_list, many=True)
    return JSONResponse(serializer.data)


def get_news_before(request, category_id, date, pk):
    news_list = News.objects.order_by('-date', '-id').filter(category_id=category_id).filter(
        Q(date__lt=date) | (Q(date=date) & Q(id__lt=pk)))[:LIMIT]
    serializer = NewsSerializer(news_list, many=True)
    return JSONResponse(serializer.data)


def get_questions(request, news_id):
    questions = Question.objects.all().filter(news_id=news_id)
    serializer = QuestionSerializer(questions, many=True)
    return JSONResponse(serializer.data)
