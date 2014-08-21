from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .models import Person, IncomingRequest, ModelObjectsTracker
from .models import CREATE_ACTION_NAME, EDIT_ACTION_NAME, DELETE_ACTION_NAME
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
        self.assertRedirects(response, reverse('index'), status_code=301, target_status_code=200)

    def test_index_view(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertTrue('person' in response.context)
        self.assertTrue(response.context['person'].user.first_name == 'Serhij')
        self.assertIn('<h1>42 Coffee Cups Test Assignment</h1>', response.content)

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
        self.assertIn('person', response.context)
        self.assertTrue(response.context['person'].user.first_name == 'Serhij')

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
        self.assertIn(SAVE_FORM_ERRORS_MESSAGE, response.content)

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
        self.assertIn(
            INVALID_LOGIN_MESSAGE.format(TEST_USERNAME, TEST_PASSWORD), response.content)

    def test_edit_link_for_not_auth_user(self):
        user = User.objects.get(pk=2)
        person = Person.objects.get(user_id=user.id)
        url = reverse('view_person',  kwargs={'person_id': person.id})
        response = self.client.get(url)
        link = '<a href="{0}">Edit</a>'.format(reverse('edit', kwargs={'person_id': person.id}))
        self.assertNotIn(link, response.content)

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
        self.assertIn(link, response.content)

    #This test fails on getBarista
    def test_request_is_stored_to_db(self):
        url = reverse('index')
        response = self.client.get(url)
        url = reverse('requests')
        response = self.client.get(url)
        requests = IncomingRequest.objects.filter(path=reverse('index'))
        self.assertTrue(requests.count() == 1)
        requests = IncomingRequest.objects.filter(path=reverse('requests'))
        self.assertTrue(requests.count() == 1)

    #This test fails on getBarista
    def test_request_view(self):
        url = reverse('index')
        response = self.client.get(url)
        url = reverse('requests')
        response = self.client.get(url)
        self.assertIn('requests', response.context)
        self.assertIn('<h4>Requests:</h4>', response.content)

    #This test fails on getBarista
    def test_model_signals(self):
        tracking_objects = ModelObjectsTracker.objects.filter(
            model_name=Person.__name__,
            type_of_event=CREATE_ACTION_NAME)
        self.assertTrue(tracking_objects.count() == 1)
        person = Person.objects.get(pk=1)
        person.skype = 'Skype Account'
        person.save()
        tracking_objects = ModelObjectsTracker.objects.filter(
            model_name=Person.__name__,
            type_of_event=EDIT_ACTION_NAME)
        self.assertTrue(tracking_objects.count() == 1)
        person.delete()
        tracking_objects = ModelObjectsTracker.objects.filter(
            model_name=Person.__name__,
            type_of_event=DELETE_ACTION_NAME)
        self.assertTrue(tracking_objects.count() == 1)

    #This test fails on getBarista
    def test_context_processor(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertIn('settings', response.context)
        url = reverse('requests')
        response = self.client.get(url)
        self.assertIn('settings', response.context)