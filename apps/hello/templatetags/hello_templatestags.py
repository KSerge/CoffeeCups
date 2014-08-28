from django import template
from django.core.urlresolvers import reverse
from ..models import Person, IncomingRequest, ModelObjectsTracker

MODEL_NAME_TO_URL_NAME = {
    Person.__name__: 'person',
    IncomingRequest.__name__: 'incomingrequest',
    ModelObjectsTracker.__name__: 'modelobjectstracker',}
register = template.Library()


def edit_link(object):
    if type(object).__name__ in MODEL_NAME_TO_URL_NAME:
        link = reverse('admin:%s_%s_change' %(object._meta.app_label,  object._meta.module_name), args=[object.id] )
    else:
        link = reverse('index')

    return {'link': link}

register.inclusion_tag('hello/link.html')(edit_link)