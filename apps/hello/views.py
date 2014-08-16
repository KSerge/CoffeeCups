from django.shortcuts import render

PERSON_RESPONSE_KEYWORD = 'person'


def index(request, person_id=1):
    return render(request, 'hello/index.html')