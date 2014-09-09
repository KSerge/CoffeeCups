from django.test import TestCase
from django.core.urlresolvers import reverse
from ..models import Person
from django.template import Template, Context

TEST_SKYPE_NAME = 'New Skype Name'
TEST_USERNAME = 'Username'
TEST_PASSWORD = 'password'


class HelloAppTestCase(TestCase):
    def test_context_processor(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertIn('settings', response.context)
        url = reverse('requests')
        response = self.client.get(url)
        self.assertIn('settings', response.context)

    def test_edit_link_template_tag(self):
        person = Person.objects.get(pk=1)
        c = Context({'person': person})
        test_template = Template("{% load hello_templatestags %} {% edit_link person %}")
        rendered = test_template.render(c)
        self.assertIn('<a href="/admin/hello/person/1/">Edit</a>', rendered)
