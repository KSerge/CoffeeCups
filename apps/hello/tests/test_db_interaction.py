from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from ..models import Person, IncomingRequest, ModelObjectsTracker
from ..models import CREATE_ACTION_NAME, EDIT_ACTION_NAME, DELETE_ACTION_NAME

TEST_SKYPE_NAME = 'New Skype Name'
TEST_USERNAME = 'Username'
TEST_PASSWORD = 'password'


class HelloAppTestCase(TestCase):
    fixtures = ['initial_data.json']

    def test_person_is_inserted(self):
        user = User.objects.get(pk=2)
        self.assertTrue(Person.objects.filter(user_id=user.id).count() == 1)

    def test_request_is_stored_to_db(self):
        url = reverse('index')
        response = self.client.get(url)
        url = reverse('requests')
        response = self.client.get(url)
        requests = IncomingRequest.objects.filter(path=reverse('index'))
        self.assertTrue(requests.count() == 1)
        requests = IncomingRequest.objects.filter(path=reverse('requests'))
        self.assertTrue(requests.count() == 1)

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