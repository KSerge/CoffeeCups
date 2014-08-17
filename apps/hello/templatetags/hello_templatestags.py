from django import template
from django.core.urlresolvers import reverse

register = template.Library()


def edit_link(person):
    return {
        'link': reverse('edit', kwargs={'person_id': person.id}),
    }

register.inclusion_tag('hello/link.html')(edit_link)