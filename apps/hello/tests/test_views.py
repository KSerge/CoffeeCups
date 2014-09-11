from django.test import TestCase
from django.core.urlresolvers import reverse
from ..models import Person, IncomingRequest
from ..views import SAVE_FORM_ERRORS_MESSAGE, INVALID_LOGIN_MESSAGE
from django.conf import settings
import os

TEST_SKYPE_NAME = 'New Skype Name'
TEST_USERNAME = 'Username'
TEST_PASSWORD = 'password'


class HelloAppTestCase(TestCase):
    fixtures = ['initial_data.json']

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

    def test_records_ordering_in_request_view(self):
        for i in range(1, 3):
            request = IncomingRequest()
            request.url = 'test' + str(i)
            request.priority = i
            request.save()
        url = reverse('requests')
        response = self.client.get(url)
        self.assertTrue(IncomingRequest.objects.all().count() == 3)
        self.assertEqual(response.context['requests'][0].priority, 2)
        self.assertEqual(response.context['requests'][1].priority, 1)
        self.assertEqual(response.context['requests'][2].priority, 0)


    # def test_register_post_valid_view(self):
    #     url = reverse('register')
    #     response = self.client.post(url, {'username': TEST_USERNAME, 'password': TEST_PASSWORD})
    #     self.assertTrue(User.objects.filter(username=TEST_USERNAME).count() == 1)
    #
    # def test_register_post_not_valid_view(self):
    #     url = reverse('register')
    #     response = self.client.post(url, {'username': TEST_USERNAME})
    #     self.assertTrue(User.objects.filter(username=TEST_USERNAME).count() == 0)