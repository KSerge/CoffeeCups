from django.core.management.base import BaseCommand
import apps.hello.models
import inspect


class Command(BaseCommand):
    help = 'Prints all project models and the count of objects in every model'

    def handle(self, *args, **options):
        for name, data in inspect.getmembers(apps.hello.models, inspect.isclass):
            try:
                objects = data.objects.all()
            except AttributeError:
                self.stderr.write('error: could not determine model %s' %name)
            else:
                self.stdout.write('Model %s: objects: %d' % (name, objects.count()))
                self.stderr.write('error: model %s: objects: %d' % (name, objects.count()))