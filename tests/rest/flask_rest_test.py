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
        self.assertEqual(len(response), 7)
        self.assertEqual(response.get('VARS_DIR'), "/variables")
        self.assertEqual(response.get('TEMPLATES_DIR'), "/data")

    @parameterized.expand([
        ("json.j2", "json.json"),
        ("yml.j2", "yml.yml")
    ])
    def test_rend_endpoint(self, template, variables):
        response = yaml.load(requests.get(self.server + f"/rend/{template}/{variables}", Loader=yaml.Loader).text)
        self.assertEqual(len(response), 3)

    @parameterized.expand([
        ("json.j2", "doesnotexists.json"),
        ("yml.j2", "doesnotexists.yml")
    ])
    def test_rend_endpoint(self, template, variables):
        expected = f"Exception([Errno 2] No such file or directory: \'/variables/{variables}\')"
        response = requests.get(self.server + f"/rend/{template}/{variables}").text
        self.assertEqual(expected, response)

    @parameterized.expand([
        ("doesnotexists.j2", "json.json"),
        ("doesnotexists.j2", "yml.yml")
    ])
    def test_rend_endpoint(self, template, variables):
        expected = f"Exception({template})"
        response = requests.get(self.server + f"/rend/{template}/{variables}").text
        self.assertEqual(expected, response)

    @parameterized.expand([
        ("standalone.j2", "variables.yml")
    ])
    def test_rendwithenv_endpoint(self, template, variables):
        payload = {'DATABASE': 'mysql56', 'IMAGE': 'latest'}
        headers = {'Content-type': 'application/json'}
        response = yaml.load(
            requests.post(self.server + f"/rendwithenv/{template}/{variables}", data=json.dumps(payload),
                          headers=headers).text, Loader=yaml.Loader)
        self.assertEqual(len(response.get("services")), 2)
        self.assertEqual(int(response.get("version")), 3)


if __name__ == '__main__':
    unittest.main()
