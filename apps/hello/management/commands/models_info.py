from django.core.management.base import BaseCommand
import inspect
import os
from django.conf import settings
from imp import load_source


class Command(BaseCommand):
    help = 'Prints all project models and the count of objects in every model'

    def handle(self, *args, **options):
        module_name_to_path_map = {}
        apps_path = os.path.join(settings.BASE_DIR, 'apps')
        for app_name in os.listdir(apps_path):
            if os.path.isdir(os.path.join(apps_path, app_name)):
                for module_name in os.listdir(os.path.join(apps_path, app_name)):
                    if os.path.isfile(os.path.join(apps_path, app_name, module_name)):
                        if module_name == 'models.py':
                            module_name_to_path_map['apps.%s.%s' % (app_name, 'models')] = \
                                os.path.join(apps_path, app_name, 'models.py')

        for module_name in module_name_to_path_map:
            try:
                module = load_source(module_name, module_name_to_path_map[module_name])
                for name, data in inspect.getmembers(module, inspect.isclass):
                    try:
                        objects = data.objects.all()
                    except AttributeError:
                        self.stderr.write('error: could not determine model %s' % name)
                    else:
                        self.stdout.write('Model %s: objects: %d' % (name, objects.count()))
                        self.stderr.write('error: model %s: objects: %d' % (name, objects.count()))
            except ImportError:
                pass
