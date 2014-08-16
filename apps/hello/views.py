from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from .models import Person

PERSON_RESPONSE_KEYWORD = 'person'


def index(request, person_id=1):
    person = get_object_or_404(Person, pk=person_id)
    request_context = RequestContext(
        request,
        {'person': person})
    return render(request, 'hello/index.html', request_context)