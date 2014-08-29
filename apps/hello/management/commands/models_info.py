from django.core.management.base import BaseCommand
# import apps.hello.models
import inspect
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Prints all project models and the count of objects in every model'

    def handle(self, *args, **options):
        models = []
        apps_path = os.path.join(settings.BASE_DIR, 'apps')
        for app_name in os.listdir(apps_path):
            if os.path.isdir(os.path.join(apps_path, app_name)):
                for module_name in os.listdir(os.path.join(apps_path, app_name)):
                    if os.path.isfile(os.path.join(apps_path, app_name, module_name)):
                        if module_name == 'models.py':
                            models.append('apps.%s.%s' % (app_name, 'models'))

        for app_models in models:
            try:
                self.stderr.write(', '.join(models))
                import app_models
                self.stderr.write(', '.join(models))
                for name, data in inspect.getmembers(app_models, inspect.isclass):
                    try:
                        objects = data.objects.all()
                    except AttributeError:
                        self.stderr.write('error: could not determine model %s' % name)
                    else:
                        self.stdout.write('Model %s: objects: %d' % (name, objects.count()))
                        self.stderr.write('error: model %s: objects: %d' % (name, objects.count()))
            except ImportError:
                pass
