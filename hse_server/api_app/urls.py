from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^categories/$', views.get_categories),
    url(r'^categories/(?P<pk>[0-9]+)/$', views.get_category),
]
