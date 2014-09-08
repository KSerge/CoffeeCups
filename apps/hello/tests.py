from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .models import Person, IncomingRequest, ModelObjectsTracker
from .models import CREATE_ACTION_NAME, EDIT_ACTION_NAME, DELETE_ACTION_NAME
from .views import SAVE_FORM_ERRORS_MESSAGE, INVALID_LOGIN_MESSAGE
from django.conf import settings
import os
from django.template import Template, Context
import time

TEST_SKYPE_NAME = 'New Skype Name'
TEST_USERNAME = 'Username'
TEST_PASSWORD = 'password'


class HelloAppTestCase(TestCase):
    fixtures = ['initial_data.json']

    def test_command_models_info(self):
        script_path = os.path.join(settings.BASE_DIR, 'collect_models_info.sh')
        os.system(script_path)
        result_file_name = time.strftime('%Y-%m-%d') + '.dat'
        script_result_path = os.path.join(settings.BASE_DIR,
                                          'script_results',
                                          result_file_name)
        self.assertTrue(os.path.isfile(script_result_path))
        f = open(script_result_path, 'r')
        file_content = ' '.join(f.readlines())
        self.assertIn('Person: objects: 1', file_content)
        f.close()

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

    def test_edit_post_valid_view(self):
        file_path = os.path.join(settings.BASE_DIR, 'apps', 'hello', 'images', 'test_image.png')
        f = open(file_path, 'r')
        post_data = {'profile_image': f, 'skype': TEST_SKYPE_NAME}
        url = reverse('edit')
        response = self.client.post(url, post_data)
        self.assertRedirects(response,
                             reverse('index'),
                             status_code=302,
                             target_status_code=200,
                             )
        self.assertTrue(Person.objects.get(pk=1).skype == TEST_SKYPE_NAME)
        f.close()
        uploaded_file_path = os.path.join(settings.BASE_DIR,
                                          'uploads',
                                          'profile',
                                          'test_image.png')
        self.assertTrue(os.path.isfile(uploaded_file_path))
        os.remove(uploaded_file_path)

    def test_edit_post_not_valid_view(self):
        url = reverse('edit')
        response = self.client.post(url, {'date_of_birth': True})
        self.assertIn(SAVE_FORM_ERRORS_MESSAGE, response.content)

    def test_login_post_valid_view(self):
        url = reverse('register')
        response = self.client.post(url, {'username': TEST_USERNAME, 'password': TEST_PASSWORD})
        url = reverse('login')
        response = self.client.post(url, {'username': TEST_USERNAME, 'password': TEST_PASSWORD})
        self.assertRedirects(response,
                             reverse('index'),
                             status_code=302,
                             target_status_code=200,
                             )

    def test_login_post_not_valid_view(self):
        url = reverse('login')
        response = self.client.post(url, {'username': TEST_USERNAME, 'password': TEST_PASSWORD})
        self.assertIn(INVALID_LOGIN_MESSAGE, response.content)

    def test_edit_link_template_tag(self):
        person = Person.objects.get(pk=1)
        c = Context({'person': person})
        test_template = Template("{% load hello_templatestags %} {% edit_link person %}")
        rendered = test_template.render(c)
        self.assertIn('<a href="/admin/hello/person/1/">Edit</a>', rendered)

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
        for x in range(0, 15):
            response = self.client.get(url)
        url = reverse('requests')
        response = self.client.get(url)
        self.assertIn('requests', response.context)
        self.assertTrue(IncomingRequest.objects.all().count() > 10)
        self.assertTrue(response.context['requests'].count() == 10)
        self.assertIn('<h4>Requests:</h4>', response.content)

    def test_model_signals(self):
        tracking_objects = ModelObjectsTracker.objects.filter(
            model_name=Person.__name__,
            type_of_event=CREATE_ACTION_NAME)
        self.assertEqual(tracking_objects.count(), 1)
        person = Person.objects.get(pk=1)
        person.skype = 'Skype Account'
        person.save()
        self.assertEqual(Person.objects.all().count(), 1)
        tracking_objects = ModelObjectsTracker.objects.filter(
            model_name=Person.__name__,
            type_of_event=EDIT_ACTION_NAME)
        # self.assertEqual(tracking_objects.count(), 1)
        person.delete()
        tracking_objects = ModelObjectsTracker.objects.filter(
            model_name=Person.__name__,
            type_of_event=DELETE_ACTION_NAME)
        self.assertEqual(tracking_objects.count(), 1)

    def test_context_processor(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertIn('settings', response.context)
        url = reverse('requests')
        response = self.client.get(url)
        self.assertIn('settings', response.context)