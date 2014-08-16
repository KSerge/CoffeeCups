from django.shortcuts import render


def index(request, person_id=1):
    return render(request, 'hello/index.html')