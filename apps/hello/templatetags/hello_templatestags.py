from django import template
from django.core.urlresolvers import reverse

register = template.Library()


def edit_link(person):
    return {
        'link': reverse('edit'),
    }

register.inclusion_tag('hello/link.html')(edit_link)