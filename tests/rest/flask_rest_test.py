#!/usr/bin/env python3
import os
import unittest

import requests
import yaml
from flask import json
from parameterized import parameterized


class FlaskServerTestCase(unittest.TestCase):
    server = os.environ.get('SERVER')

    def test_env_endpoint(self):
        response = json.loads(requests.get(self.server + "/env").text)
        self.assertGreaterEqual(len(response), 7)
        self.assertEqual(response.get('VARS_DIR'), "/variables")
        self.assertEqual(response.get('TEMPLATES_DIR'), "/data")

    @parameterized.expand([
        ("json.j2", "json.json"),
        ("yml.j2", "yml.yml")
    ])
    def test_rend_endpoint_p(self, template, variables):
        response = yaml.safe_load(requests.get(self.server + f"/render/{template}/{variables}").text)
        self.assertEqual(len(response), 3)

    @parameterized.expand([
        ("json.j2", "doesnotexists.json"),
        ("yml.j2", "doesnotexists.yml")
    ])
    def test_rend_endpoint_doesnotexist(self, template, variables):
        expected = f"Exception([Errno 2] No such file or directory: \'/variables/{variables}\')"
        response = requests.get(self.server + f"/render/{template}/{variables}").text
        self.assertEqual(expected, response)

    @parameterized.expand([
        ("doesnotexists.j2", "json.json"),
        ("doesnotexists.j2", "yml.yml")
    ])
    def test_rend_endpoint(self, template, variables):
        expected = f"Exception({template})"
        response = requests.get(self.server + f"/render/{template}/{variables}").text
        self.assertEqual(expected, response)

    @parameterized.expand([
        ("standalone.j2", "variables.yml")
    ])
    def test_rendwithenv_endpoint(self, template, variables):
        payload = {'DATABASE': 'mysql56', 'IMAGE': 'latest'}
        headers = {'Content-type': 'application/json'}
        response = yaml.safe_load(
            requests.post(self.server + f"/render/{template}/{variables}", data=json.dumps(payload),
                          headers=headers).text)
        self.assertEqual(len(response.get("services")), 2)
        self.assertEqual(int(response.get("version")), 3)


if __name__ == '__main__':
    unittest.main()
