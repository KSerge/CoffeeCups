from django.contrib import admin
from .models import Person, IncomingRequest, ModelObjectsTracker

admin.site.register(Person)
admin.site.register(IncomingRequest)
admin.site.register(ModelObjectsTracker)
