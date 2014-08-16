from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .models import Person, IncomingRequest
from .views import PERSON_RESPONSE_KEYWORD, REQUESTS_RESPONSE_KEYWORD


class HelloAppTestCase(TestCase):
    fixtures = ['initial_data.json']

    def test_person_is_inserted(self):
        user = User.objects.get(pk=2)
        self.assertTrue(Person.objects.filter(user_id=user.id).count() == 1)

    def test_default_view(self):
        url = reverse('default')
        response = self.client.get(url)
        self.assertTrue(response.context['person'].user.first_name == 'Serhij')
        self.assertTrue('<h1>42 Coffee Cups Test Assignment</h1>' in response.content)

    def test_index_view(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertTrue(PERSON_RESPONSE_KEYWORD in response.context)
        self.assertTrue(response.context[PERSON_RESPONSE_KEYWORD].user.first_name == 'Serhij')
        self.assertTrue('<h1>42 Coffee Cups Test Assignment</h1>' in response.content)

    def test_edit_get_view(self):
        url = reverse('view_person', kwargs={'person_id': 1})
        response = self.client.get(url)
        self.assertTrue(PERSON_RESPONSE_KEYWORD in response.context)
        self.assertTrue(response.context[PERSON_RESPONSE_KEYWORD].user.first_name == 'Serhij')

    def test_request_is_stored_to_db(self):
        url = reverse('index')
        response = self.client.get(url)
        url = reverse('requests')
        response = self.client.get(url)
        requests = IncomingRequest.objects.filter(path=reverse('index'))
        self.assertTrue(requests.count() == 1)
        requests = IncomingRequest.objects.filter(path=reverse('requests'))
        self.assertTrue(requests.count() == 1)

    def test_request_view(self):
        url = reverse('index')
        response = self.client.get(url)
        url = reverse('requests')
        response = self.client.get(url)
        self.assertTrue(REQUESTS_RESPONSE_KEYWORD in response.context)
        self.assertTrue('<h4>Requests:</h4>' in response.content)
