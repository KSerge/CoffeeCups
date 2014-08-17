from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .models import Person, IncomingRequest
from .views import PERSON_RESPONSE_KEYWORD, REQUESTS_RESPONSE_KEYWORD, CONTEXT_SETTINGS_KEYWORD
from .views import SAVE_FORM_ERRORS_MESSAGE, INVALID_LOGIN_MESSAGE

TEST_SKYPE_NAME = 'New Skype Name'
TEST_USERNAME = 'Username'
TEST_PASSWORD = 'password'


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

    def test_context_processor(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertTrue(CONTEXT_SETTINGS_KEYWORD in response.context)
        url = reverse('requests')
        response = self.client.get(url)
        self.assertTrue(CONTEXT_SETTINGS_KEYWORD in response.context)

    def test_register_post_valid_view(self):
        url = reverse('register')
        response = self.client.post(url, {'username': TEST_USERNAME, 'password': TEST_PASSWORD})
        self.assertTrue(User.objects.filter(username=TEST_USERNAME).count() == 1)

    def test_register_post_not_valid_view(self):
        url = reverse('register')
        response = self.client.post(url, {'username': TEST_USERNAME})
        self.assertTrue(User.objects.filter(username=TEST_USERNAME).count() == 0)

    def test_edit_get_view(self):
        url = reverse('view_person', kwargs={'person_id': 1})
        response = self.client.get(url)
        self.assertTrue(PERSON_RESPONSE_KEYWORD in response.context)
        self.assertTrue(response.context[PERSON_RESPONSE_KEYWORD].user.first_name == 'Serhij')

    def test_edit_post_valid_view(self):
        url = reverse('edit', kwargs={'person_id': 1})
        response = self.client.post(url, {'skype': TEST_SKYPE_NAME})
        self.assertRedirects(response,
                             reverse('view_person', kwargs={'person_id': 1}),
                             status_code=302,
                             target_status_code=200,
                             )
        self.assertTrue(Person.objects.get(pk=1).skype == TEST_SKYPE_NAME)

    def test_edit_post_not_valid_view(self):
        url = reverse('edit', kwargs={'person_id': 1})
        response = self.client.post(url, {'date_of_birth': True})
        self.assertTrue(SAVE_FORM_ERRORS_MESSAGE in response.content)

    def test_login_post_valid_view(self):
        url = reverse('register')
        response = self.client.post(url, {'username': TEST_USERNAME, 'password': TEST_PASSWORD})
        url = reverse('login')
        response = self.client.post(url, {'username': TEST_USERNAME, 'password': TEST_PASSWORD})
        user = User.objects.get(username=TEST_USERNAME)
        person = Person.objects.get(user_id=user.id)
        self.assertRedirects(response,
                             reverse(
                                 'view_person',
                                 kwargs={'person_id': person.id}),
                             status_code=302,
                             target_status_code=200,
                             )

    def test_login_post_not_valid_view(self):
        url = reverse('login')
        response = self.client.post(url, {'username': TEST_USERNAME, 'password': TEST_PASSWORD})
        self.assertTrue(INVALID_LOGIN_MESSAGE.format(TEST_USERNAME, TEST_PASSWORD) in response.content)

    def test_edit_link_for_not_auth_user(self):
        user = User.objects.get(pk=2)
        person = Person.objects.get(user_id=user.id)
        url = reverse('view_person',  kwargs={'person_id': person.id})
        response = self.client.get(url)
        link = '<a href="{0}">Edit</a>'.format(reverse('edit', kwargs={'person_id': person.id}))
        self.assertFalse(link in response.content)

    def test_edit_link_for_auth_user(self):
        url = reverse('register')
        response = self.client.post(url, {'username': TEST_USERNAME, 'password': TEST_PASSWORD})
        url = reverse('login')
        response = self.client.post(url, {'username': TEST_USERNAME, 'password': TEST_PASSWORD})
        user = User.objects.get(username=TEST_USERNAME)
        person = Person.objects.get(user_id=user.id)
        url = reverse('view_person',  kwargs={'person_id': person.id})
        response = self.client.get(url)
        link = '<a href="{0}">Edit</a>'.format(reverse('edit', kwargs={'person_id': person.id}))
        self.assertTrue(link in response.content)