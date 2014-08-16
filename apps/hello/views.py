from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from .models import Person, IncomingRequest
from django.conf import settings
from .forms import PersonForm, UserForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

PERSON_RESPONSE_KEYWORD = 'person'
REQUESTS_RESPONSE_KEYWORD = 'requests'
CONTEXT_SETTINGS_KEYWORD = 'settings'
SAVE_FORM_ERRORS_MESSAGE = 'Some Errors Occurred'
INVALID_LOGIN_MESSAGE = 'Invalid login details: {0}, {1}'


def context_processor(request):
    return {
        CONTEXT_SETTINGS_KEYWORD: settings,
    }


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


def register_user(request):
    message = ''
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        person_form = PersonForm(data=request.POST)
        if user_form.is_valid() and person_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            person = person_form.save(commit=False)
            person.user = user
            person.save()
            return HttpResponseRedirect(reverse('view_person', kwargs={'person_id': person.id}))
        else:
            message = SAVE_FORM_ERRORS_MESSAGE
    else:
        user_form = UserForm()
        person_form = PersonForm()

    request_context = RequestContext(
        request,
        {
            'user_form': user_form,
            'person_form': person_form,
            'message': message
        })
    return render(request, 'hello/register.html', request_context)


def login_user(request):
    return render(request, 'hello/login.html')


def edit(request, person_id):
    return render(request, 'hello/edit.html')