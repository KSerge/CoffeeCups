from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save, post_delete

CREATE_ACTION_NAME = 'created'
EDIT_ACTION_NAME = 'edited'
DELETE_ACTION_NAME = 'deleted'


class Person(models.Model):
    user = models.OneToOneField(User, null=True)
    date_of_birth = models.DateField(auto_now=False, null=True, blank=True)
    bio = models.CharField(max_length=254, null=True, blank=True)
    jabber = models.EmailField(max_length=100, null=True, blank=True)
    skype = models.CharField(max_length=50, null=True, blank=True)
    other_contacts = models.CharField(max_length=254, null=True, blank=True)
    profile_image = models.ImageField(upload_to="profile", null=True, blank=True)


class IncomingRequest(models.Model):
    path = models.CharField(max_length=500)
    visiting_date = models.DateTimeField(auto_now=True)
    priority = models.PositiveSmallIntegerField(default=0)


class ModelObjectsTracker(models.Model):
    model_name = models.CharField(max_length=50, null=False, blank=False)
    type_of_event = models.CharField(max_length=10, null=False, blank=False)
    created_date = models.DateTimeField(default=timezone.now())

MODEL_NAMES = (Person.__name__, IncomingRequest.__name__,)


def get_sender_name(sender):
    if sender.__name__ in MODEL_NAMES:
        return sender.__name__
    else:
        return ''


def model_objects_insert_edit_callback(sender, created, **kwargs):
    model_name = get_sender_name(sender)
    if not model_name:
        return

    tracker = ModelObjectsTracker()
    tracker.model_name = model_name
    if created:
        tracker.type_of_event = CREATE_ACTION_NAME
    else:
        tracker.type_of_event = EDIT_ACTION_NAME
    tracker.save()


def model_objects_delete_callback(sender, **kwargs):
    model_name = get_sender_name(sender)
    if not model_name:
        return

    tracker = ModelObjectsTracker()
    tracker.model_name = model_name
    tracker.type_of_event = DELETE_ACTION_NAME
    tracker.save()

post_save.connect(model_objects_insert_edit_callback, sender=Person)
post_save.connect(model_objects_insert_edit_callback, sender=IncomingRequest)
post_delete.connect(model_objects_delete_callback, sender=Person)
post_delete.connect(model_objects_delete_callback, sender=IncomingRequest)