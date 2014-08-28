from django import template
from django.core.urlresolvers import reverse
from ..models import Person, IncomingRequest

MODEL_NAME_TO_URL_NAME = {Person.__name__: 'person', }
register = template.Library()

def edit_link(object):
    # person/1/
    
    return {
        'link': reverse('edit'),
    }

register.inclusion_tag('hello/link.html')(edit_link)