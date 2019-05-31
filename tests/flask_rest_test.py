#!/usr/bin/env python3
import os
import unittest

import requests
from flask import json


class FlaskServerTestCase(unittest.TestCase):
    server = "http://0.0.0.0:5000"

    def test_env_endpoint(self):
        response = json.loads(requests.get(self.server + "/env").text)
        self.assertEqual(len(response), 7)
        self.assertEqual(response.get('VARS_DIR'), os.environ['VARS_DIR'])
        self.assertEqual(response.get('TEMPLATES_DIR'), os.environ['TEMPLATES_DIR'])


if __name__ == '__main__':
    unittest.main()
