from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^categories/$', views.get_categories),
    url(r'^categories/(?P<pk>[0-9]+)/$', views.get_category),
    url(r'^news/(?P<category_id>[0-9]+)/$', views.get_news),
    url(r'^news/(?P<category_id>[0-9]+)/(?P<date>[0-9]+)/(?P<pk>[0-9]+)/$', views.get_news_before),
]
