from django.conf.urls import url
from .views import register_user, login_user, user_logout, edit, view_requests, index

urlpatterns = [
    url(r'^register/$', register_user, name='register'),
    url(r'login/$', login_user, name='login'),
    url(r'^logout/$', user_logout, name='logout'),
    url(r'^edit/(?P<person_id>\w+)/$', edit, name='edit'),
    url(r'^edit/$', edit, name='edit'),
    url(r'^requests/$', view_requests, name='requests'),
    url(r'^(?P<person_id>\w+)/$', index, name='view_person'),
    url(r'^$', index, name='index'),
]