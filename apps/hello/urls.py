from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^hello/register/$', register_user, name='register'),
    url(r'hello/login/$', login_user, name='login'),
    url(r'^hello/logout/$', user_logout, name='logout'),
    url(r'^hello/edit/(?P<person_id>\w+)/$', edit, name='edit'),
    url(r'^hello/requests/$', view_requests, name='requests'),
    url(r'^hello/(?P<person_id>\w+)/$', index, name='view_person'),
    url(r'^$', index, name='default'),
    url(r'^hello/$', index, name='index'),
]