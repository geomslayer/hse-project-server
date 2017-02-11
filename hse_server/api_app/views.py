from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Category, News
from .serializers import CategorySerializer, NewsSerializer


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
