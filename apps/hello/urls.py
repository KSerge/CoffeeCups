from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^hello/(?P<person_id>\w+)/$', index, name='view_person'),
    url(r'^$', index, name='default'),
    url(r'^hello/$', index, name='index'),
]