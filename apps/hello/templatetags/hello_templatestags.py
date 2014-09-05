from django import template
from django.core.urlresolvers import reverse

register = template.Library()


def edit_link(object):
    link = reverse(
        'admin:%s_%s_change' %(object._meta.app_label,object._meta.module_name),
        args=[object.id])
    return {'link': link}

register.inclusion_tag('hello/link.html')(edit_link)