from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from .models import Person, IncomingRequest
from django.conf import settings
from .forms import PersonForm, UserForm, UserEditForm, IncomingRequestFormset
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json

SAVE_FORM_ERRORS_MESSAGE = 'Some Errors Occurred'
INVALID_LOGIN_MESSAGE = 'Invalid login details'


def context_processor(request):
    return {
        'settings': settings,
    }


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
    stored_requests = IncomingRequest.objects.order_by('priority', 'visiting_date')[0:10]
    request_context = RequestContext(
        request,
        {'requests': stored_requests})
    return render(request, 'hello/requests.html', request_context)

#
# def edit_requests(request):
#     distinct_requests = IncomingRequest.objects.values('path').distinct()
#     initial_data = []
#     for record in distinct_requests:
#         initial_data.append({'path': record['path']})
#     formset = IncomingRequestFormset(initial=initial_data)
#
#     if request.method == 'POST':
#         formset = IncomingRequestFormset(request.POST)
#         if formset.is_valid():
#             priority_dict = {}
#             for item in formset.cleaned_data:
#                 priority_dict[item['path']] = item['priority']
#             requests = IncomingRequest.objects.all()
#             for item in requests:
#                 item.priority = priority_dict.get(item.path, 0)
#                 item.save()
#             return HttpResponseRedirect(reverse('requests'))
#
#     request_context = RequestContext(
#         request,
#         {'requests': distinct_requests, 'formset': formset},)
#     return render(request, 'hello/edit_requests.html', request_context)


def register_user(request):
    message = ''
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        person_form = PersonForm(data=request.POST)
        if user_form.is_valid() and person_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            return HttpResponseRedirect(reverse('index'))
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
    message = ''
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                message = "Your account is disabled"
        else:
            message = INVALID_LOGIN_MESSAGE
    else:
        user_form = UserForm()

    request_context = RequestContext(
        request,
        {
            'form': user_form,
            'message': message
        })

    return render(request, 'hello/login.html', request_context)


def edit(request):
    try:
        person = Person.objects.get(pk=1)
        user = User.objects.get(pk=person.user_id)
    except Person.DoesNotExist, User.DoesNotExists:
        person = Person()
        user = User()
    message = ''
    if request.method == 'POST':
        person_form = PersonForm(request.POST, request.FILES, instance=person)
        user_form = UserEditForm(request.POST, instance=user)
        if user_form.is_valid() and person_form.is_valid():
            user_form.save()
            person_form.save()
            if request.is_ajax():
                data = {'redirect_url': reverse('index')}
                return HttpResponse(json.dumps(data), content_type="application/json")
            return HttpResponseRedirect(reverse('index'))
        else:
            message = SAVE_FORM_ERRORS_MESSAGE
    else:
        person_form = PersonForm(instance=person)
        user_form = UserEditForm(instance=user)

    request_context = RequestContext(
        request,
        {
            'person': person,
            'person_form': person_form,
            'user_form': user_form,
            'message': message
        })
    return render(request, 'hello/edit.html', request_context)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))