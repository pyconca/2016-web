import os
import glob
import unittest

import yaml
import json

from flask import Flask

from web.app import create_app
from web.utils import get_data_file

app = create_app()


class TestSyntax(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.test_client = self.app.test_client()

    def test_data_files(self):
        data_files = []
        data_files += glob.glob(os.path.join(self.app.config['APP_PATH'],
                                                 'data', '*.json'))
        data_files += glob.glob(os.path.join(self.app.config['APP_PATH'],
                                                 'data', '*.yml'))

        for data_file in data_files:
            with self.app.app_context():
                get_data_file(os.path.basename(data_file))
