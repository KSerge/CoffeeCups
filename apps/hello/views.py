from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from .models import Person, IncomingRequest

PERSON_RESPONSE_KEYWORD = 'person'
REQUESTS_RESPONSE_KEYWORD = 'requests'
CONTEXT_SETTINGS_KEYWORD = 'settings'


def index(request, person_id=1):
    try:
        person = Person.objects.get(pk=person_id)
    except Person.DoesNotExist:
        person = Person()
    request_context = RequestContext(
        request,
        {PERSON_RESPONSE_KEYWORD: person})
    return render(request, 'hello/index.html', request_context)


def view_requests(request):
    stored_requests = IncomingRequest.objects.order_by('visiting_date')[0:10]
    request_context = RequestContext(
        request,
        {REQUESTS_RESPONSE_KEYWORD: stored_requests})
    return render(request, 'hello/requests.html', request_context)