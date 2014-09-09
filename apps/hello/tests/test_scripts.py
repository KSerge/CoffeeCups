from django.test import TestCase
from django.conf import settings
import os
import time


class HelloAppTestCase(TestCase):
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