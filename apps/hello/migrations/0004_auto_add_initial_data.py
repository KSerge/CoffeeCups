from south.v2 import DataMigration
from django.conf import settings
import os
from django.core.management import call_command


class Migration(DataMigration):

    def forwards(self, orm):
        file_path = os.path.join(settings.BASE_DIR, 'apps', 'hello', 'fixtures', 'initial_data.json')
        call_command("loaddata", file_path)
