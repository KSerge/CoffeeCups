from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from .models import Person, IncomingRequest

PERSON_RESPONSE_KEYWORD = 'person'


def index(request, person_id=1):
    try:
        person = Person.objects.get(pk=person_id)
    except Person.DoesNotExist:
        person = Person()
    request_context = RequestContext(
        request,
        {'person': person})
    return render(request, 'hello/index.html', request_context)


def view_requests(request):
    return render(request, 'hello/requests.html')